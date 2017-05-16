var express = require('express');
var router = express.Router();

/* GET home page. */
//connectMongo();
router.get('/test', function(req, res, next) {
  //res.send(connectMongo());
  res.render('index', { title: 'Express' });
});
/* GET Userlist page. */
router.get('/', function(req, res) {

    var results_from_mongo = [];
    var db = req.db;
    var collection = db.get('clustered');
    var str = db.collection('clustered').find();
    collection.find({},{},function(e,docs){

      //results_from_mongo.push(docs);
      res.render('index', {
          'stuff': results_from_mongo
      });
    });
});

router.get('/:cluster/:license/:status', function(req, res) {

    var results_from_mongo = [];
    var db = req.db;
    var collection = db.get('clustered');
    var str = db.collection('clustered').find();
    var cluster = req.params.cluster;
    var license = req.params.license;
    var status = req.params.status;
    if(status == "Open"){
      status = "";
    }
    else{
      status = {$ne:""};
    }
    if(cluster=='taxi'){
      cluster = "TAXI/DRIVER";
      collection.find({$and:[{"Cluster Label" : cluster},{"Current License Status" : "LICENSE " + license}, {"Business Close Date":status}]},{},function(e,docs){

        results_from_mongo.push(docs);
        res.render('index', {
            'stuff': results_from_mongo
        });
      });
    }
    else if(cluster == 'cleaning'){
      collection.find({$and:[{$or:[{"Cluster Label" : "CLEANING"},{"Cluster Label" : "JANITORIAL"}]},{"Current License Status" : "LICENSE " + license}, {"Business Close Date":status}]},{},function(e,docs){

        results_from_mongo.push(docs);
        res.render('index', {
            'stuff': results_from_mongo
        });
      });
    }
    else if(cluster == 'beauty'){
      collection.find({$and:[{$or:[{"Cluster Label" : "HAIR/STYLIST"},{"Cluster Label" : "BEAUTY/SALON"},{"Cluster Label" : "SALON/HAIR"}]},{"Current License Status" : "LICENSE " + license}, {"Business Close Date":status}]},{},function(e,docs){

        results_from_mongo.push(docs);
        res.render('index', {
            'stuff': results_from_mongo
        });
      });
    }
    else if(cluster == 'food'){
      collection.find({$and:[{$or:[{"Cluster Label" : "FOOD"},{"Cluster Label" : "RESTAURANT"}]},{"Current License Status" : "LICENSE " + license}, {"Business Close Date":status}]},{},function(e,docs){

        results_from_mongo.push(docs);
        res.render('index', {
            'stuff': results_from_mongo
        });
      });
    }
    else if(cluster == 'maintenancerepair'){
        collection.find({$and:[{$or:[{"Cluster Label" : "REPAIR"},{"Cluster Label" : "MAINTENANCE"}]},{"Current License Status" : "LICENSE " + license}, {"Business Close Date":status}]},{},function(e,docs){

          results_from_mongo.push(docs);
          res.render('index', {
              'stuff': results_from_mongo
          });
        });
    }
    else if(cluster=='CommercialRental'){
      cluster = "COMMERCIAL/RENTAL";
      collection.find({$and:[{"Cluster Label" : cluster},{"Current License Status" : "LICENSE " + license}, {"Business Close Date":status}]},{},function(e,docs){

        results_from_mongo.push(docs);
        res.render('index', {
            'stuff': results_from_mongo
        });
      });
    }
    else if(cluster=='ResidentialRental'){
      cluster = "RESIDENTIAL/RENTAL";
      collection.find({$and:[{"Cluster Label" : cluster},{"Current License Status" : "LICENSE " + license}, {"Business Close Date":status}]},{},function(e,docs){

        results_from_mongo.push(docs);
        res.render('index', {
            'stuff': results_from_mongo
        });
      });
    }

});
module.exports = router;
