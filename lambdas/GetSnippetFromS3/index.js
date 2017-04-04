'use strict';

console.log('Loading function');

const aws = require('aws-sdk');

const s3 = new aws.S3({ apiVersion: '2006-03-01' });


exports.handler = (event, context, callback) => {
    const key = event.pathParameters.user_id + "/" + event.pathParameters.snippet_id;
    const bucket = process.env.BucketName;

    const params = {
        Bucket: bucket,
        Key: key
    };
    s3.getObject(params, (err, data) => {
        if (err) {
            const message = `Error getting object ${params.Key} from bucket ${bucket}`;
            callback(message);
            context.fail({
                statusCode: 400,
                headers: {
                    'Access-Control-Allow-Origin': '*',
                },
            });

        } else {
            const object = data.Body.toString();
            context.succeed({
                statusCode: 200,
                headers: {
                    'Access-Control-Allow-Origin': '*',
                },
                body: object,
            });
        }
    });
};
