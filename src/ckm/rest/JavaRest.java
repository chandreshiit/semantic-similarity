package ckm.rest;


import java.util.HashMap;
import java.util.Map;
import demo.gradle.HelloGradle;
import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;

import org.json.simple.JSONObject;

import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

// Plain old Java Object it does not extend as class or implements
// an interface

// The class registers its methods for the HTTP GET request using the @GET annotation.
// Using the @Produces annotation, it defines that it can deliver several MIME types,
// text, XML and HTML.

// The browser requests per default the HTML MIME type.

//Sets the path to base URL + /hello
@Path("/hello")
public class JavaRest{

  // This method is called if TEXT_PLAIN is request
  @GET
  @Produces("text/plain")
  public String sayPlainTextHello() {
    return  "hi atri";
  }

  // This method is called if XML is request
  @GET
  @Produces("text/xml")
  public String sayXMLHello() {
    return "<?xml version=\"1.0\"?>" + "<hello> Hello Jersey xml" + "</hello>";
  }

  // This method is called if HTML is request
  @GET
  @Produces("text/html")
  public String sayHtmlHello() {
    return "<html> " + "<title>" + "Hello Jersey" + "</title>"

      + "<body><h1>" + "Hello Jersey" + "</body></h1>" + "</html> ";
  }
  
  // this method is called if json is requested
  @SuppressWarnings("unchecked")
  @POST
  @Produces("application/json")
  @Consumes("application/json")
  public String sayjsonHello(String data) throws Exception {
	    System.out.println(data);
		JSONParser parser = new JSONParser();
		JSONObject jobj =  (JSONObject) parser.parse(data);
		//System.out.println(jobj.toString());
		String candidates =  HelloGradle.getCandidates(jobj);
//		System.out.println(jobj.get("query"));
        return candidates;
  }
  

}
