const aws = require('aws-sdk');
const s3 = new aws.S3({ apiVersion: '2006-03-01'});

const bucketName = process.env.BucketName;

const parsers = {}
parsers['python3'] = require('./python3.min');
parsers['java8'] = require('./java8.min');

function updateSnippet (data) {
  language = data.snippetLanguage || 'python3';
  data.AST = parsers[language](data.snippet, () => {}, {});
}

exports.myHandler = function (event, context) {
  const params = {
    Bucket: bucketName,
  }
  s3.listObjects(params, (err, data) => {
    if (err) console.log(err);
    keys = data.Contents.map(o => o.Key).filter(k => k.indexOf("index.json") < 0);
    keys.forEach(key => {
      const params = {
        Bucket: bucketName,
        Key: key,
      };
      s3.getObject(params, (_, data) => {
        const snippet = JSON.parse(data.Body);
        updateSnippet(snippet);
        const params = {
          Bucket: bucketName,
          Key: key,
          Data: JSON.stringify(snippet)
        }
        s3.putObject(params)
      })
    })
  })
}
