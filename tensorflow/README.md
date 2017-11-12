# Usage
You need to hand pick photos in folder X with its subfolders, each named after a tag. 

For example, we have collected 215 photos from Festive Road as `festival-of-giants-2017`,
in which three folders contains more than 20 photos each.

```
constume 27
generic 78
puppet 20
```

## Caveats
For this to work, make sure each subfolder has at least 20 different photos.
For examples, the following folders have been removed:
```
bees 4
butterfly 1
canvas 4
catepillar 1
cycle 3
dragon 5
drummer 7
event 1
fly 6
goose 16
harminder 18
hummingbirds 13
installation 6
mechanism 6
triceratops 5
```
They can still be found in the `festival-of-giants-2017-all` folder.

# Installation

Issue commands as follows: 
```
git clone https://github.com/mkhackathon/festive-road-tagging \
 && cd festive-road-tagging \
 && git pull origin retraining \
 && git checkout retraining \
 && cd tensorflow
```

# Output of training

Issue the following command for training:
```
b training festival-of-giants-2017
```

```
INFO:tensorflow:Looking for images in 'costume'
INFO:tensorflow:Looking for images in 'generic'
INFO:tensorflow:Looking for images in 'puppet'
INFO:tensorflow:100 bottleneck files created.
INFO:tensorflow:2017-11-12 21:56:09.271068: Step 0: Train accuracy = 40.0%
INFO:tensorflow:2017-11-12 21:56:09.271325: Step 0: Cross entropy = 1.028333
INFO:tensorflow:2017-11-12 21:56:10.059672: Step 0: Validation accuracy = 29.0% (N=100)
INFO:tensorflow:2017-11-12 21:56:14.422290: Step 10: Train accuracy = 94.0%
INFO:tensorflow:2017-11-12 21:56:14.422540: Step 10: Cross entropy = 0.699466
INFO:tensorflow:2017-11-12 21:56:14.893748: Step 10: Validation accuracy = 90.0% (N=100)
INFO:tensorflow:2017-11-12 21:56:19.288959: Step 20: Train accuracy = 93.0%
INFO:tensorflow:2017-11-12 21:56:19.289188: Step 20: Cross entropy = 0.621012
INFO:tensorflow:2017-11-12 21:56:19.753360: Step 20: Validation accuracy = 88.0% (N=100)
INFO:tensorflow:2017-11-12 21:56:23.625095: Step 30: Train accuracy = 90.0%
...
INFO:tensorflow:2017-11-12 22:26:07.714672: Step 3960: Train accuracy = 99.0%
INFO:tensorflow:2017-11-12 22:26:07.714902: Step 3960: Cross entropy = 0.020156
INFO:tensorflow:2017-11-12 22:26:08.088241: Step 3960: Validation accuracy = 93.0% (N=100)
INFO:tensorflow:2017-11-12 22:26:11.873447: Step 3970: Train accuracy = 98.0%
INFO:tensorflow:2017-11-12 22:26:11.873674: Step 3970: Cross entropy = 0.027538
INFO:tensorflow:2017-11-12 22:26:12.245750: Step 3970: Validation accuracy = 91.0% (N=100)
INFO:tensorflow:2017-11-12 22:26:16.007040: Step 3980: Train accuracy = 100.0%
INFO:tensorflow:2017-11-12 22:26:16.007269: Step 3980: Cross entropy = 0.010003
INFO:tensorflow:2017-11-12 22:26:16.367913: Step 3980: Validation accuracy = 87.0% (N=100)
INFO:tensorflow:2017-11-12 22:26:19.996361: Step 3990: Train accuracy = 100.0%
INFO:tensorflow:2017-11-12 22:26:19.996588: Step 3990: Cross entropy = 0.029551
INFO:tensorflow:2017-11-12 22:26:20.356557: Step 3990: Validation accuracy = 89.0% (N=100)
INFO:tensorflow:2017-11-12 22:26:23.834799: Step 3999: Train accuracy = 100.0%
INFO:tensorflow:2017-11-12 22:26:23.835032: Step 3999: Cross entropy = 0.021235
INFO:tensorflow:2017-11-12 22:26:24.216097: Step 3999: Validation accuracy = 92.0% (N=100)
INFO:tensorflow:Final test accuracy = 100.0% (N=13)
INFO:tensorflow:Froze 2 variables.
Converted 2 variables to const ops.
```

We want to test the following image:
![A puppet](https://scripts.njae.me.uk/festive-road-pictures/small/2017/festival-of-giants-2017/19424271_10155798955468912_3425389609817707195_n-small.jpg)

# Outputs of testing
Issue the following command for testing:
```
b testing festival-of-giants-2017 puppet/19424271_10155798955468912_3425389609817707195_n-small.jpg
```

```
2017-11-12 22:27:28.363361: W tensorflow/core/framework/op_def_util.cc:334] Op BatchNormWithGlobalNormalization is deprecated. It will cease to work in GraphDef version 9. Use tf.nn.batch_normalization().
puppet (score = 0.99616)
costume (score = 0.00312)
generic (score = 0.00072)
```
