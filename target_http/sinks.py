"""http target sink class, which handles writing streams."""

from __future__ import annotations

from singer_sdk.sinks import RecordSink
import logging

class httpSink(RecordSink):
    """http target sink class."""
    def __init__(self, target, stream_name, schema, key_properties):
        
        super().__init__(target=target, stream_name=stream_name, schema=schema, key_properties=key_properties)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
    def process_record(self, record: dict, context: dict) -> None:

        url = self.config.get('url')
        
        # Headers
        headers = self.config.get('headers', {})
    
        # HTTP Method
        method = self.config.get('method', 'GET') 
        if method == 'GET':
            # Static query parameters
            queryParams = self.config.get('queryParams', {})
            
            # Dynamically map some 
            self.req = Request('GET', url, headers=headerObject)
        elif method == 'POST':  
            self.req = Request('POST', url, headers=headerObject, data=record)
        
        # TLS Properties
        tls = self.config.get('tls', {"skip_verify": False})
        
        # Certificates
        cert_file_path = tls.get('cert_file_path')
        key_file_path = tls.get('key_file_path')
        cacert_file_path = tls.get('cacert_file_path')
        
        self.session = self.req.Session()
        if self.cert_file_path and self.key_file_path:
            self.session.cert = (self.cert_file_path, self.key_file_path)
        
        # TLS Verification
        if tls.get('skip_verify', False):
            self.session.verify = False
        elif self.cacert_file_path:
            self.session.verify = self.cacert_file_path
            
        # Send the request and get the response
        prepared_req = self.req.prepare()
        response = self.session.send(prepared_req)
                
        # Log the response
        if response.status_code > 299:
            error = response.error()
            self.logger.error(f"Failed to write record {record} to {url}: {error}")
        else:
            self.logger.info(f"Successfully wrote record {record} to {url}")    
