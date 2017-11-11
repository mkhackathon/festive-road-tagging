import clarifai2.api.ClarifaiBuilder;
import clarifai2.api.ClarifaiClient;
import clarifai2.dto.input.ClarifaiInput;
import clarifai2.dto.model.output.ClarifaiOutput;
import clarifai2.dto.prediction.Concept;

import java.util.List;

public class ClarifaiConnector {
    ClarifaiClient client = new ClarifaiBuilder("d7539dafbab3450792bc82d530d42e18").buildSync();


    List<Concept> getTagsFromUrl(String url){
        List<ClarifaiOutput<Concept>> predictionResults =client.getDefaultModels().generalModel() // You can also do client.getModelByID("id") to get your custom models
                .predict()
                .withInputs(
                        ClarifaiInput.forImage(url))
                .executeSync()
                .get();

        return predictionResults.get(0).data();

    }


}

