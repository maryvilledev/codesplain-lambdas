'use strict';

console.log('Loading function');

const aws = require('aws-sdk');
const s3 = new aws.S3({ apiVersion: '2006-03-01' });
const lamda = new aws.Lambda({
    region: 'us-west-2',
});

// Helper for invoking the callback in handler func
const sendResponse = (callback, statusCode, response) => {
  callback(null, {
    statusCode,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    body: `{ "response": "${response}" }`,
  })
}

// Saves the given Body to the given Bucket under the given Key. Returns a Promise.
const saveToS3 = (Bucket, Key, Body) => {
  const params = {
      Bucket,
      Key,
      Body,
  };
  return new Promise((resolve, reject) => {
    s3.putObject(params, (err, data) => {
      if (err) reject(err);
      resolve({ Key });
    });
  });
}

exports.handler = (event, context, callback) => {
  // Extract some stuff that we need from the request object.
  const accessToken = event.headers.Authorization;
  const userID      = event.pathParameters.user_id;

  // Invoke the authorization lambda to ensure the accessToken
  // included in the request matches the userID for the requested
  // resource.
  const authorizeTokenName = process.env.authorizeTokenName;
  lamda.invoke({
    FunctionName: authorizeTokenName,
    Payload: JSON.stringify({
        accessToken,
        userID,
    }),
  }, (err, data) => {
    // Handle the error if the AuthorizeToken lambda failed
    // to finish properly.
    if (err) {
      console.log(err);
      sendResponse(callback, '500', 'Failed to update snippet.');
    }

    const payload = JSON.parse(data.Payload);
    // If authorization failed, response with a 400
    if (payload.statusCode === '400') {
      console.log(payload.body);
      sendResponse(callback, '400', payload.body);
    }

    /* ----- Otherwise, save to S3 ----- */
    const snippetID = event.pathParameters.snippet_id;
    const key       = `${userID}/${snippetID}`;
    const apiID     = event.requestContext.apiId;
    const bucket    = process.env.BucketName;

    saveToS3(bucket, key, event.body)
      .then(key => {
        callback(null, {
          statusCode: '200',
          headers: {
            'Access-Control-Allow-Origin': '*',
          },
          body: `{ "key": "${snippetID}" }`,
        });
      })
      .catch(err => {
        const msg = `Error putting object ${key} into bucket ${bucket}`;
        console.err(msg);
        sendResponse(callback, '500', msg);
      });
  });
};
