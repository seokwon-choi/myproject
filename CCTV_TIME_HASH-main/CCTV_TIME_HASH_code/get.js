const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;
const bodyParser = require('body-parser');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.listen(PORT, () => {
                        console.log(`Server started on port ${PORT}`)
});


app.post('/find', (req, res) => {
                        const time = req.body.time || '';

const Eos = require('eosjs');
const HASH = 'hashtable';
const ALICE = 'alice';

const eos = Eos({
                keyProvider:'5JowXhXj8A6fKZtYgXCCtEykKyVZoMZ4DyUAjSRyCVG7pFWCM21'
});

let options = {
                authorization: ALICE+'@active',
                broadcast: true,
                sign: true
}

const TIME = time;

async function foo()
{
 return await eos.getTableRows({json: true, scope: HASH, code: HASH, table: "hashes", limit: 1,lower_bound: TIME, upper_bound:TIME});

}
(async () => {
        return res.send((await foo()).rows[0])
})()
});
