const functions = require('firebase-functions');
// Imports the Google Cloud client library
const vision = require('@google-cloud/vision')();
const moment = require('moment');
const gcs = require('@google-cloud/storage')();
const fs = require('fs');

// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
// exports.helloWorld = functions.https.onRequest((request, response) => {
//  response.send("Hello from Firebase!");
// });

// The Cloud Functions for Firebase SDK to create Cloud Functions and setup triggers.

// The Firebase Admin SDK to access the Firebase Realtime Database.
const firebase = require('firebase-admin');
firebase.initializeApp(functions.config().firebase);

function HistorianData(imageId, date, op) {
    this.imageId = imageId;
    this.date = date;
    this.operation = op;
}

function Item() {
    this.historian = [];
    this.count = 0;
}

function updateItem(name, url, filePath) {
  // Read item
  firebase.database().ref("items").child(name).once("value", function(snapshot) {
    var add = filePath.includes('in')
    console.log("FilePath: " + filePath + " contains 'in':" + add)
    dbItem = snapshot.val()
    console.log("dbItem: " + JSON.stringify(dbItem))

    if (dbItem) {
      // Item is added (add) or removed (remove)
      var hist = new HistorianData(url, moment().format(), 'remove')
      if (add) {
        hist.operation = 'add'
      }
      // Create new item
      var updatedItem = new Item()
      // Get old historian data and finally add (push) this process
      if (dbItem.historian) {
        updatedItem.historian = updatedItem.historian.concat(dbItem.historian)
      }
      updatedItem.historian.push(hist)
      // Get old count and increase / descrease accordiently
      updatedItem.count = dbItem.count
      if (add) {
        updatedItem.count++
      } else {
        updatedItem.count--
      }
      // If we have less or equal than 0 items, remove them from the DB
      if (updatedItem.count <= 0) {
        console.log("Deleted Item: " + JSON.stringify(updatedItem))
        snapshot.ref.remove()
      } else {
        console.log("Updated Item: " + JSON.stringify(updatedItem))
        snapshot.ref.set(updatedItem)
      }
    } else {
      createItem(name, url)
    }
  }, function (errorObject) {
    console.log("The read failed: " + errorObject.code);
  });
}

function createItem(name, url) {
  var hist = new HistorianData(url, moment().format(), 'add')
  var item = new Item()
  item.historian = hist
  item.count = 1
  console.log("CreateItem: " + JSON.stringify(item))
  firebase.database().ref("items/" + name).set(item)
}

function decideWhatIsShownInTheImage(detections, fileBucket, filePath) {
  var labels = detections.labels
  var logos = detections.logos
  var text = detections.text
  var documents = detections.documents


  if (labels) {
    for (var i=0; i<labels.length; i++) {
      if(labels[i]=="apple" || labels[i]=="banana" || labels[i]=="cola"|| labels[i]=="milk"|| labels[i]=="orange"){
        updateItem(labels[i], fileBucket + '/' + filePath, filePath)
      }
  }
  console.log(JSON.stringify(labels))
  }
  if (logos) {
    //console.log(JSON.stringify(logos))
  }
  if (text) {
    //console.log(JSON.stringify(text))
  }
  if (documents) {
    //console.log(JSON.stringify(documents))
  }
}

function analyzeImage(fileBucket, filePath) {
  const file = gcs.bucket(fileBucket).file(filePath);

  var types = ['document', 'labels', 'logos', 'text']

  vision.detect(file, types, function(err, detections, apiResponse) {
    // if no error, process result
    if (!err) {
      decideWhatIsShownInTheImage(detections, fileBucket, filePath)
    } else {
      console.log('Error: ' + JSON.stringify(err))
    }
  });

}

exports.newImageUploaded = functions.storage.object().onChange(event => {
  const object = event.data; // The Storage object.

  const fileBucket = object.bucket; // The Storage bucket that contains the file.
  const filePath = object.name; // File path in the bucket.
  const contentType = object.contentType; // File content type.
  const resourceState = object.resourceState; // The resourceState is 'exists' or 'not_exists' (for file/folder deletions).
  const metageneration = object.metageneration; // Number of times metadata has been generated. New objects have a value of 1.

  // Exit if this is triggered on a file that is not an image.
  if (!contentType.startsWith('image/')) {
    console.log('This is not an image.');
    return;
  }

  // Exit if this is a move or deletion event.
  if (resourceState === 'not_exists') {
    console.log('This is a deletion event.');
    return;
  }

  // Exit if file exists but is not new and is only being triggered
  // because of a metadata change.
  if (resourceState === 'exists' && metageneration > 1) {
    console.log('This is a metadata change event.');
    return;
  }

  analyzeImage(fileBucket, filePath)

});

exports.reqItem = functions.https.onRequest((req, res) => {
  myJson = require("./visionapi.json");
  console.log('Returning the request with' + myJson);
  res.status(200).send(myJson);
});
