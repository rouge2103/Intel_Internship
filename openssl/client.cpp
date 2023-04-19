#include <openssl/ssl.h>
#include <openssl/err.h>
#include <iostream>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>

using namespace std;

/*
-- describe the TLS_client_method
-- difference between ca.pem, and client.crt
-- what are the different error codes for each step
-- trust store location (ideally a well known location
-- api to specify the list of ciphers that are agreeable for the client
-- api for specifying the heartbeat
-- check if there is a possibility to retrieve the session-key from the ssl object, and use it to ressurect a possible dead connection
-- what is the idea of caching?
*/

void ShowCerts(SSL* ssl)
{
    X509* cert;
    string line;

    cert = SSL_get_peer_certificate(ssl); /* get the server's certificate */
    if (cert != NULL)
    {
        cout<<"Server certificates:\n";
        line = X509_NAME_oneline(X509_get_subject_name(cert), 0, 0);
        cout<<line<<endl;
        line = X509_NAME_oneline(X509_get_issuer_name(cert), 0, 0);
        cout<<"Issuer: \n"<<line<<endl;
        X509_free(cert);     /* free the malloc'ed certificate copy */
    }
    else
        cout<<"No certificates.\n";
}


int main() {
	//initialization
    SSL_library_init();
    SSL_load_error_strings();
    OpenSSL_add_all_algorithms();
    SSL_CTX *ctx = SSL_CTX_new(TLS_client_method());
    char buf[1024];
    if (!ctx) {
    	cout<<"Error-CTX\n";
        // handle error
    }
    const char *cipher_list = "TLS_AES_256_GCM_SHA384";
    if(SSL_CTX_set_ciphersuites(ctx, cipher_list)!=1){
        // error
        SSL_CTX_free(ctx);
        return 1;
    }

    // Load the trusted CA certificates
    /*if (SSL_CTX_load_verify_locations(ctx, "ca.pem", NULL) != 1) {
        // handle error
    }*/
    // Load the client certificate and private key
    if (SSL_CTX_use_certificate_file(ctx, "client1.crt", SSL_FILETYPE_PEM) != 1) {
    	cout<<"ERROR-Certificate File\n";
        // handle error
    }
    if (SSL_CTX_use_PrivateKey_file(ctx, "client1.key", SSL_FILETYPE_PEM) != 1) {
    	cout<<"ERROR-Private Key\n";
        // handle error
    }
  
    SSL *ssl = SSL_new(ctx);
    if (!ssl) {
    	cout<<"ERROR-SSL\n";
        // handle error
    }
  
  
	//setting up the socket to connect to the server
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        // handle error
    }
    else
    {
    	cout<<"Socket is created\n";
    }
    struct sockaddr_in server_address;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(2056);
    if(inet_pton(AF_INET, "127.0.0.1", &server_address.sin_addr)<=0)
    {
    	cout<<"ERROR-pton\n";
    }
    cout<<"Harsh\n";
    if (connect(sockfd, (struct sockaddr *) &server_address, sizeof(server_address)) ==-1) {
    	cout<<"ERROR-Connect\n";
        // handle error
    }
    else 
    {
    	cout<<"Client is connected\n";
    }
  
    SSL_set_fd(ssl, sockfd);
    int ret;
    if (ret=SSL_connect(ssl) != 1) {
    	cout<<"ERROR-SSL Connect\n";
        // handle error
    }
    else
    {
    	cout<<"SSL Connected\n";
    	cout<<SSL_get_ciphers(ssl)<<endl;
    	ShowCerts(ssl);
    }
    //sleep(2);
    // Code to send data over the SSL connection
    // Data to be sent
    const char *data = "This is the message sent by client";
    int data_len = strlen(data);
  
    // Encrypt and send the data
    ret = SSL_write(ssl, data, data_len);
    if (ret > 0) {
    	cout<<"Write successful\n";
        // handle error
    }
    int bytes = SSL_read(ssl, buf, sizeof(buf));
    if(bytes>0)
    {
     	printf("Server Msg: %.*s \n", bytes,buf);
    }
    // Teardown pshase
    SSL_shutdown(ssl);
    SSL_free(ssl);
    SSL_CTX_free(ctx);
    close(sockfd);
  
    return 0;
}
