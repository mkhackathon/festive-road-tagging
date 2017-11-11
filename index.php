<?php

include 'vendor/autoload.php';

use PhpFanatic\clarifAI\ImageClient;

$api_key     = 'd273be677bd54a6699b9cd24d6f36228';
$count       = 100; // Set amount of images to generate tags for.
$file        = __DIR__ . '/festive-road-tagging/festival-of-giants-2017-hand-tags.json';
$output_name = '/random_with_tags_added.json';
$result      = file_get_contents($file);
$result      = json_decode($result, TRUE);

$new = [];

$count = $count ?: count($file);

function imageTags($image, &$new, $i, $api_key) {

    $client = new ImageClient($api_key);

    $client->AddImage($image['url']);

    $result = $client->Predict();

    $result = json_decode($result, TRUE);

    $result = $result['outputs'][0]['data']['concepts'];

    if (!empty($result)) {

        $tags = [];

        foreach ($result as $tag) {
            $tags[] = $tag['name'];
        }

        $image['tags'] = $tags;
        $new[$i] = $image;

    } else {
        finish($new);
        echo 'Completed early at - ' . (count($new) + 1);
        die();
    }
}

function finish($new, $output_name)
{
    $new = json_encode($new, JSON_PRETTY_PRINT);
    file_put_contents(__DIR__ . '/' . $output_name, $new);
}

for ($i = 0; $i < $count; $i++) {
    imageTags($result[$i], $new, $i, $api_key);
    echo $i . ' has been added to array' . "\n";
}

finish($new, $output_name);
echo 'Completed!';
