const aws = require('aws-sdk');
const s3 = new aws.S3({ apiVersion: '2006-03-01'});

const bucketName = process.env.BucketName;

const parsers = {}
parsers['python3'] = require('./python3');

const updateSnippet = (data) => {
  data.AST = parsers[data.snippetLanguage](data.snippet, () => {}, {});
}

const listAllKeys = async () => {
  var params = {
    Bucket: bucketName,
  }
  const keys = await s3.listObjects(params, (_, data) => (
    //Remember to ignore index files
    data.map(o => o.Contents.Key).filter(k => k.indexOf("index.json") < 0)
  ));
  return keys;
}

const getData = async (key) => {
  var params = {
    Bucket: bucketName,
    Key: key
  }
  const data = await s3.getObject(params, (_, data) => (
    JSON.parse(data.body)
  ));
  return data
}

const saveData = (key, data) => {
  var params = {
    Bucket: bucketName,
    Key: key,
    Body: JSON.stringify(data)
  };
  s3.putObject(params);
}

exports.myHandler = async (event, context) {
  listAllKeys().forEach(key => {
    let data = await getData(key);
    await updateSnippet(data);
    await saveData(key, data);
  })
}
