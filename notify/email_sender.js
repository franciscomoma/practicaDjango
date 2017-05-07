var amqp = require('amqplib/callback_api');

amqp.connect('amqp://localhost', function(err, conn) {
    conn.createChannel(function(err, ch) {
        var exchange = 'emails';

        ch.assertExchange(exchange, 'fanout', {durable: false});

        ch.assertQueue('', {exclusive: true}, function(err, q) {
        console.log(" [*] Waiting for emails. To exit press CTRL+C", q.queue);

        ch.bindQueue(q.queue, exchange, '');

        ch.consume(q.queue, process_email_callback, {noAck: true});
        });
    });
});

function process_email_callback(response){
    email_json = response.content.toString()
    email = JSON.parse(email_json);

    console.log("SENDING FAKE EMAIL:")
    console.log("===============================================")
    console.log("Subject: " + email.subject)
    console.log("to: " + email.to)
    console.log("Message: " + email.message)
    console.log("===============================================")
}