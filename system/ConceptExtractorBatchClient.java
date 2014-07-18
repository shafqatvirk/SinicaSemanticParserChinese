//import semanticrolelabeling.*;
import java.io.*;
import edu.stanford.nlp.trees.Tree;
import java.util.*;
import java.io.File;
import java.io.FileReader;
import opennlp.maxent.DataStream;
import opennlp.maxent.PlainTextByLineDataStream;

//package bdn;
/*  The java.net package contains the basics needed for network operations. */
import java.net.*;
/* The java.io package contains the basics needed for IO operations. */
import java.io.*;
/** The SocketClient class is a simple example of a TCP/IP Socket Client.
 *
 */

public class ConceptExtractorBatchClient
{
    
    
	public static void main(String[] args)
    {
    /** Define a host server */
    String host = "localhost";
    /** Define a port */
    int port = 29999;
    System.out.println("SocketClient initialized");
	
		try
        {	
			//System.out.println("Debug: Entered try."); //Andy add 20140522 for debug
			//File dir = new File("../input");
			//File[] directoryListing = dir.listFiles();
			//if (directoryListing != null) {
			//for (File child : directoryListing) {
			// Do something with child
			BufferedReader inputReader = new BufferedReader(new FileReader("../input/input2.txt"));
			//BufferedReader inputReader = new BufferedReader(new FileReader(child));
			
			PrintWriter outputFileWriter = new PrintWriter("../output/output.txt", "UTF-8");
			//outputFileWriter.println("<rdf:RDF xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\">");
			//outputFileWriter.println("<rdf:Description rdf:about=\"http://sentic.net/challenge/sentence\">");
			outputFileWriter.close();
			String sent;
			System.out.println("Processing....");
			
			while ((sent = inputReader.readLine()) != null)
			{
			//System.out.println("Sentence: "+sent);
			//System.out.println("Parsing....");
			String sentence = sent + (char) 13;
			
			InetAddress address = InetAddress.getByName(host);
			// Establish a socket connetion 
			Socket connection = new Socket(address, port);
			BufferedOutputStream bos = new BufferedOutputStream(connection.
			getOutputStream());
			//OutputStreamWriter osw = new OutputStreamWriter(bos, "US-ASCII");
			OutputStreamWriter osw = new OutputStreamWriter(bos,"cp1252");
			osw.write(sentence);
			osw.flush();
			//System.out.println("Concept Extraction....");
			BufferedReader fromServer = new BufferedReader(
       		new InputStreamReader(connection.getInputStream()));
			String serverResponse = fromServer.readLine();
			//System.out.println(serverResponse);
			Runtime rlabeler = Runtime.getRuntime();

			//----VVVV--- Andy Lee add 20140522 for transfering sentence to python program.
			File wfile2 = new File("../temp/sent-output.txt");
        	BufferedWriter wr2 = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(wfile2),"UTF-8"));
        	String toFileString = sent;
        	wr2.write(toFileString);
        	wr2.flush();
        	wr2.close();
        	//----^^^^--- Andy Lee add 20140522 for transfering sentence to python program.

            //String srlClassifier = "python concept-formulator2.py " + '"'+sent+'"' ;
			String srlClassifier = "python concept-formulator.py " + '"'+sent+'"' ;
			Process p = rlabeler.exec(srlClassifier);
            BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
            p.waitFor();
            //System.out.println("here i am");
			String line2;
			while((line2 = br.readLine()) != null) {
				System.out.println(line2);
			//while (br.ready())
               // System.out.println(br.readLine());
			  }
			
           // }
			
			//}
		} 
		
		//FileWriter fstream = new FileWriter("../output/output.txt", true); //true tells to append data.
		//BufferedWriter outFileWriter;
		//outFileWriter = new BufferedWriter(fstream);
		//outFileWriter.write("</rdf:Description>");
		//outFileWriter.write("\n</rdf:RDF>");
		//outFileWriter.close();
		System.out.println("Done!");
		// else {
				// Handle the case where dir is not really a directory.
				// Checking dir.isDirectory() above would not be sufficient
				// to avoid race conditions with another process that deletes
				// directories.
			//}
		}
        catch (Exception e)
        {
		String cause = e.getMessage();
		if (cause.equals("python: not found"))
			System.out.println("No python interpreter found.");
		else
			System.out.println("Error: "+cause); //Andy add 20140522 for error handling.
        }
    }
}