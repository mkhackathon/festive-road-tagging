
import clarifai2.dto.prediction.Concept;
import com.flickr4java.flickr.Flickr;
import com.flickr4java.flickr.RequestContext;
import com.flickr4java.flickr.auth.Auth;
import com.flickr4java.flickr.auth.AuthInterface;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import com.flickr4java.flickr.auth.Permission;
import com.flickr4java.flickr.uploader.UploadMetaData;
import com.flickr4java.flickr.uploader.Uploader;
import org.apache.commons.io.FileUtils;
import org.scribe.model.Token;
import org.scribe.model.Verifier;

public class Application {

    public static void main(String[] args) {
        try {
            URL url = new URL("https://scripts.njae.me.uk/festive-road-pictures/full-size/2017/Harminder%202017/29341669790_df9c56c6f4_k.jpg");
            File photoFile = new File("/Users/Abu/tmp/tmp.jpg");
            List <String> tags = new ArrayList<String>();
            ClarifaiConnector connector = new ClarifaiConnector();
            List<Concept> concepts =  connector.getTagsFromUrl(url.toExternalForm());
            for(Concept concept: concepts){
                tags.add(concept.name());
            }
//            FileUtils.copyURLToFile(url, photoFile);


            FlickrConnector flickrConnector = new FlickrConnector();
            Flickr flickr = flickrConnector.getFlickr();

            Flickr.debugStream = false;
            AuthInterface authInterface = flickr.getAuthInterface();

            Scanner scanner = new Scanner(System.in);
            Token token = authInterface.getRequestToken();
            System.out.println("token: " + token);

            String authUrl = authInterface.getAuthorizationUrl(token, Permission.WRITE);
            System.out.println("Follow this URL to authorise yourself on Flickr");
            System.out.println(authUrl);
            System.out.println("Paste in the token it gives you:");
            System.out.print(">>");
            String tokenKey = scanner.nextLine();
            scanner.close();

            Token requestToken = authInterface.getAccessToken(token, new Verifier(tokenKey));

            System.out.println("Authentication success");

            Auth auth = authInterface.checkToken(requestToken);
            System.out.println("Token: " + requestToken.getToken());
            System.out.println("Secret: " + requestToken.getSecret());
            System.out.println("nsid: " + auth.getUser().getId());
            System.out.println("Realname: " + auth.getUser().getRealName());
            System.out.println("Username: " + auth.getUser().getUsername());
            System.out.println("Permission: " + auth.getPermission().getType());


            RequestContext.getRequestContext().setAuth(auth);
            Uploader uploader =  flickr.getUploader();

            UploadMetaData uploadMetaData = new UploadMetaData();
            uploadMetaData.setPublicFlag(true);
            uploadMetaData.setTitle("Test Image");
            uploadMetaData.setTags(tags);
            Path path = Paths.get(photoFile.getAbsolutePath());
            uploader.upload(Files.readAllBytes(path),uploadMetaData);

        } catch (Exception fe){
            System.out.println(fe.getMessage());
        }
    }




}

