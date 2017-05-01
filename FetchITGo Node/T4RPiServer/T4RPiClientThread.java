package org.eclipse.californium.examples;

import java.lang.Thread;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.concurrent.TimeUnit;
import java.lang.InterruptedException;
import java.util.concurrent.TimeUnit;
import java.lang.InterruptedException;

import org.eclipse.californium.core.CoapClient;
import org.eclipse.californium.core.CoapResponse;
import org.eclipse.californium.core.Utils;

public class T4RPiClientThread extends Thread {
	public static void main(String args[]) {
            	T4RPiClientThread t = new T4RPiClientThread();
            	t.start();
        }

        public void run() {
		while(true) {
            		client();
            		// thread will have a sleep time of 10 second
            		try {
                		TimeUnit.SECONDS.sleep(10);
            		} catch(InterruptedException ex) {
                		System.out.println("\nClient Restarted\n");
            		}
		}
        }

    	public void client() {
        	URI uri = null; // URI parameter of the request

        	// input URI from command line arguments
        	try {
            		uri = new URI("coap://api.tantiv4.com:5683/endpoint/keepalive");
        	} catch (URISyntaxException e) {
            		System.err.println("Invalid URI: " + e.getMessage());
            		System.exit(-1);
        	}
        	CoapClient client = new CoapClient(uri);
        	//JSONObject body = new JSONObject();
        	//body.put("device_id", "rpi1");
        	CoapResponse response = client.post("{\"device_id\":\"t4rpi1\"}", 1);

        	if (response!=null) {
            		System.out.println(response.getCode());
            		System.out.println(response.getOptions());
            		System.out.println(response.getResponseText());

            		System.out.println("\nADVANCED\n");
            		// access advanced API with accesUs to more details through .advanced()
            		System.out.println(Utils.prettyPrint(response));
        	} else {
            		System.out.println("No response received.");
        	}
    	}
}

