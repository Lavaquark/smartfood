
const vision = require('@google-cloud/vision')();

const filePath = 'http://www.duden.de/_media_/full/B/Banane-201020047719.jpg'
var types = [
  'crops',
  'document',
  'faces',
  'landmarks',
  'labels',
  'logos',
  'properties',
  'safeSearch',
  'similar',
  'text'
]
console.log(vision)
vision.detect(filePath, types, function(err, detections, apiResponse) {
  console.log(detections)
});
