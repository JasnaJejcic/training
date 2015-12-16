var isPrime = require('is-number-prime');

exports.handler = function(event, context) {
    console.log('Testing number: ' + event.number);

    if (isPrime(event.number)) {
        context.succeed('You found a prime!');
    } else {
        context.fail('Better luck next time!');
    }
}