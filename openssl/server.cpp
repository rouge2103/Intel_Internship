#include <openssl/ssl.h>
#include <openssl/err.h>
#include <iostream>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <string.h>

using namespace std;

//list of ciphers that are supported is a capability of TLS1.3
//they are:
//TLS_AES_256_GCM_SHA384
//TLS_CHACHA20_POLY1305_SHA256
//TLS_AES_128_GCM_SHA256
//TLS_AES_128_CCM_8_SHA256
//TLS_AES_128_CCM_SHA256
//specify that I need a client certificate
//there will be a dev/ops step to estabilsh the trust store with the root certificates
//better that if the brokers get their own certificates from the CA-Authority


int main() {
    SSL_library_init();
    SSL_load_error_strings();
    OpenSSL_add_all_algorithms();
    
    SSL_CTX *ctx = SSL_CTX_new(TLS_server_method());
    //SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER|SSL_VERIFY_FAIL_IF_NO_PEER_CERT, NULL);
    if (!ctx) {
    	cout<<"ERROR- CTX\n";
        // handle error
    }
  
    // set the preferred cipher list
    const char *cipher_list = "TLS_AES_256_GCM_SHA384";
    if(SSL_CTX_set_ciphersuites(ctx, cipher_list)!=1){
        // error
        SSL_CTX_free(ctx);
        return 1;
    }
    
    // load the server certificate and private key
    if (SSL_CTX_use_certificate_file(ctx, "server1.crt", SSL_FILETYPE_PEM) != 1) {
    	cout<<"ERROR- Certificate file\n";
        // handle error
    }
    if (SSL_CTX_use_PrivateKey_file(ctx, "server1.key", SSL_FILETYPE_PEM) != 1) {
    	cout<<"ERROR-Private Key\n";
        // handle error
    }
    
    if (!SSL_CTX_check_private_key(ctx))
    {
        cout<<"Private key does not match the public certificate\n";
        
    }
    
    //SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER | SSL_VERIFY_FAIL_IF_NO_PEER_CERT, NULL);
    //SSL_CTX_set_verify_depth(ctx, 4);
  	
  	
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        // handle error
    }
    else
    {
    	cout<<"Socket is created\n";
    }
    
  	
    struct sockaddr_in server_address, client_address;
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(2056);
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
  
    if (bind(sockfd, (struct sockaddr *) &server_address, sizeof(server_address)) < 0) 
    {
    	cout<<"ERROR- bind\n";
    
        // handle error
    }
  
    if (listen(sockfd, 32) < 0) 
    {
    	cout<<"ERROR-Listen\n";
        // handle error
    }
    else
    {
    	cout<<"Server is listeining\n";
    }
    
    while (true) {
        socklen_t client_len = sizeof(client_address);
        int client_sock = accept(sockfd, (struct sockaddr *) &client_address, &client_len);
        char buf[1024];
        if (client_sock < 0) 
        {
        	cout<<"ERROR--Client sock\n";
            // handle error
        }
        else 
        {
        	cout<<"client is connected\n";
        }
        SSL *ssl = SSL_new(ctx);
        if (!ssl) {
            // handle error
            cout<<"ERROR-SSL\n";
        }

        // binding ssl structure to connection 
        SSL_set_fd(ssl, client_sock);
        // performing SSL/TLS handshake
        if (SSL_accept(ssl)<=0) {
        	
        	cout<<"ERROR-SSL Accept\n";
        	
            // handle error
        }
        else
        {
        	cout<<"SSL Accepted\n";
        }
        
        int bytes = SSL_read(ssl, buf, sizeof(buf));
        if(bytes>0)
        {
        	printf("Client Msg: %.*s \n", bytes,buf);
        }
        const char *data = "This is the message sent by server";
    	int data_len = strlen(data);
        int ret = SSL_write(ssl, data, data_len);
    	if (ret >0) {
    	cout<<"Write successful\n";
    	}
        // Teardown phase
        SSL_shutdown(ssl);
        SSL_free(ssl);
        close(client_sock);
    }
    
    // free socket
    SSL_CTX_free(ctx);
    close(sockfd);
  
    return 0;
}
