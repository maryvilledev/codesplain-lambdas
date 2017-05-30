const aws = require('aws-sdk');
const s3 = new aws.S3({ apiVersion: '2006-03-01'});

const bucketName = process.env.BucketName;

const parsers = {}
parsers['python3'] = require('./python3.min');
parsers['java8'] = require('./java8.min');

function updateSnippet (data) {
  data.AST = parsers[data.snippetLanguage](data.snippet, () => {}, {});
}

function listAllKeys () {
  var params = {
    Bucket: bucketName,
  }
  const keys = s3.listObjects(params, (_, data) => (
    //Remember to ignore index files
    data.map(o => o.Contents.Key).filter(k => k.indexOf("index.json") < 0)
  ));
  return keys;
}

function getData (key) {
  var params = {
    Bucket: bucketName,
    Key: key
  }
  const data = s3.getObject(params, (_, data) => (
    JSON.parse(data.body)
  ));
  return data
}

function saveData(key, data) {
  var params = {
    Bucket: bucketName,
    Key: key,
    Body: JSON.stringify(data)
  };
  s3.putObject(params);
}

exports.myHandler = function (event, context) {
  listAllKeys().forEach(key => {
    let data = getData(key);
    updateSnippet(data);
    saveData(key, data);
  })
}
