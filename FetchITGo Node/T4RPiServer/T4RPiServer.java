/*******************************************************************************
 * Copyright (c) 2015 Institute for Pervasive Computing, ETH Zurich and others.
 * 
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * and Eclipse Distribution License v1.0 which accompany this distribution.
 * 
 * The Eclipse Public License is available at
 *    http://www.eclipse.org/legal/epl-v10.html
 * and the Eclipse Distribution License is available at
 *    http://www.eclipse.org/org/documents/edl-v10.html.
 * 
 * Contributors:
 *    Matthias Kovatsch - creator and main architect
 *    Kai Hudalla (Bosch Software Innovations GmbH) - add endpoints for all IP addresses
 ******************************************************************************/
package org.eclipse.californium.examples;

import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.SocketException;
import java.util.List;
import java.util.logging.Level;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.concurrent.TimeUnit;
import java.lang.InterruptedException;
import java.lang.Thread;

import org.eclipse.californium.core.CoapClient;
import org.eclipse.californium.core.CaliforniumLogger;
import org.eclipse.californium.core.CoapResponse;
import org.eclipse.californium.core.CoapResource;
import org.eclipse.californium.core.CoapServer;
import org.eclipse.californium.core.network.CoapEndpoint;
import org.eclipse.californium.core.network.EndpointManager;
import org.eclipse.californium.core.network.config.NetworkConfig;
import org.eclipse.californium.core.server.resources.CoapExchange;
import org.eclipse.californium.core.Utils;

import org.eclipse.californium.examples.T4RPiClientThread;

public class T4RPiServer extends CoapServer {

	static {
            CaliforniumLogger.initialize();
            CaliforniumLogger.setLevel(Level.CONFIG);
	}
	private static final int COAP_PORT = NetworkConfig.getStandard().getInt(NetworkConfig.Keys.COAP_PORT);
	public static Integer PORT ;
        public static String device_payload;
    /*
     * Application entry point.
     */
    public static void main(String[] args) {
        
        try {

            // create server
            T4RPiServer server = new T4RPiServer();
            // add endpoints on all IP addresses
            server.addEndpoints();
            PORT = COAP_PORT;//5683;//non secure port
            T4RPiClientThread clientthread = new T4RPiClientThread();
            clientthread.start(); 
            server.start();

        } catch (SocketException e) {
            System.err.println("Failed to initialize server: " + e.getMessage());
        }
    }
    
    /**
     * Add individual endpoints listening on default CoAP port on all IPv4 addresses of all network interfaces.
     */
    private void addEndpoints() {
    	for (InetAddress addr : EndpointManager.getEndpointManager().getNetworkInterfaces()) {
            // only binds to IPv4 addresses and localhost
            if (addr instanceof Inet4Address || addr.isLoopbackAddress()) {
                InetSocketAddress bindToAddress = new InetSocketAddress(addr, COAP_PORT);
                addEndpoint(new CoapEndpoint(bindToAddress));
            }
	}
    }

    /*
     * Constructor for a new Hello-World server. Here, the resources
     * of the server are initialized.
     */
    public T4RPiServer() throws SocketException {
        
        // provide an instance of a notify resource
        add(new NotifyResource());
        add(new DeviceResource());
        add(new ModeResource());
        add(new FetchitHealthResource());
        add(new GatewayHealthResource());
    }

    /*
     * Definition of the Notify Resource
     */
    class NotifyResource extends CoapResource {
        
        public NotifyResource() {
            
            // set resource identifier
            super("raspberry");
            
            // set display name
            getAttributes().setTitle("Raspberry Resource");
        }

	public void handlePOST(final CoapExchange exchange) {

            List<String> path = exchange.advanced().getRequest().getOptions().getUriPath();
            String ip_addr = exchange.getSourceAddress().getHostAddress();
            System.out.println("DeviceStatusResouce POST------------ : from " + ip_addr + ":" + " payload ");
            String data = new String(exchange.getRequestPayload());
            System.out.println("DeviceStatusResouce POST------------ : payload " + data);

            System.err.println("DeviceStatusResouce POST : " + path.toString() + " from " + ip_addr);
            exchange.respond("{\"result\":\"OK\"}");
            //todo - invoke raspberry pi device control 
	}
        
        @Override
        public void handleGET(CoapExchange exchange) {
            
            // respond to the request
            exchange.respond("Raspberry");
        }
    }

    /*
     * Definition of the Device Resource
     */
    class DeviceResource extends CoapResource {
	public DeviceResource() {
            super("device");
            getAttributes().setTitle("Device Resource");
	}

	@Override
	public void handleGET(CoapExchange exchange) {
            exchange.respond(device_payload);
	}

	@Override
	public void handlePOST(CoapExchange exchange) {
            List<String> path = exchange.advanced().getRequest().getOptions().getUriPath();
            String ip_addr = exchange.getSourceAddress().getHostAddress();
            System.out.println("DeviceStatusResouce POST------------ : from " + ip_addr + ":" + " payload ");
            String data = new String(exchange.getRequestPayload());
            System.out.println("DeviceStatusResouce POST------------ : payload " + data);
            device_payload = data;
            System.err.println("DeviceStatusResouce POST : " + path.toString() + " from " + ip_addr);
            exchange.respond("{\"result\":\"OK\"}");
	}
    }   

    /*
     * Definition of the Mode Resource
     */
    class ModeResource extends CoapResource {
	public ModeResource() {
            super("mode");
            getAttributes().setTitle("Mode Resource");
	}

	@Override
	public void handleGET(CoapExchange exchange) {
            exchange.respond("mode");
	}

	@Override
	public void handlePOST(CoapExchange exchange) {
            List<String> path = exchange.advanced().getRequest().getOptions().getUriPath();
            String ip_addr = exchange.getSourceAddress().getHostAddress();
            System.out.println("DeviceStatusResouce POST------------ : from " + ip_addr + ":" + " payload ");
            String data = new String(exchange.getRequestPayload());
            System.out.println("DeviceStatusResouce POST------------ : payload " + data);
            System.err.println("DeviceStatusResouce POST : " + path.toString() + " from " + ip_addr);
            exchange.respond("{\"result\":\"OK\"}");
	}
    }

    /*
     * Definition of the Fetchit Health Resource
     */
    class FetchitHealthResource extends CoapResource {
	public FetchitHealthResource() {
            super("fetchit_health");
            getAttributes().setTitle("Fetchit Health Resource");
	}

	@Override
	public void handleGET(CoapExchange exchange) {
            exchange.respond("fetchit_health");
	}

	@Override
	public void handlePOST(CoapExchange exchange) {
            List<String> path = exchange.advanced().getRequest().getOptions().getUriPath();
            String ip_addr = exchange.getSourceAddress().getHostAddress();
            System.out.println("DeviceStatusResouce POST------------ : from " + ip_addr + ":" + " payload ");
            String data = new String(exchange.getRequestPayload());
            System.out.println("DeviceStatusResouce POST------------ : payload " + data);
            System.err.println("DeviceStatusResouce POST : " + path.toString() + " from " + ip_addr);
            exchange.respond("{\"result\":\"OK\"}");
	}
    }

    /*
     * Definition of the Gateway Health Resource
     */
    class GatewayHealthResource extends CoapResource {
	public GatewayHealthResource() {
            super("gateway_health");
            getAttributes().setTitle("Gateway Health Resource");
	}

	@Override
	public void handleGET(CoapExchange exchange) {
            exchange.respond("gateway_health");
	}

	@Override
	public void handlePOST(CoapExchange exchange) {
            List<String> path = exchange.advanced().getRequest().getOptions().getUriPath();
            String ip_addr = exchange.getSourceAddress().getHostAddress();
            System.out.println("DeviceStatusResouce POST------------ : from " + ip_addr + ":" + " payload ");
            String data = new String(exchange.getRequestPayload());
            System.out.println("DeviceStatusResouce POST------------ : payload " + data);
            System.err.println("DeviceStatusResouce POST : " + path.toString() + " from " + ip_addr);
            exchange.respond("{\"result\":\"OK\"}");
	}
    }

}
