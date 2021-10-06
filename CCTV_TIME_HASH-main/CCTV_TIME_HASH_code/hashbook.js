const express = require('express');
const app = express();
const PORT = process.env.PORT || 5000;
const bodyParser = require('body-parser');

app.use(bodyParser.text());
app.use(bodyParser.urlencoded({extended: true}));
app.listen(PORT, () => {
                        console.log(`Server started on port ${PORT}`)
});

//let time=2
//let hash='a'

//global.time = time;
//global.hash = hash;

//const input = require("fs").readFileSync('/dev/stdin').toString().split(' ')

app.post('/hash', (req, res) => {
                const time = req.body.time || '';
                const hash = req.body.hash || '';


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
const HASH_value = hash;

eos.contract(HASH).then(hashBookContract =>{
                const rows = {
                                user: ALICE,
                                time: TIME,
                                hash: HASH_value
                }
        hashBookContract.insert(rows, options).then(response => {
                //      console.log(response)
                        console.log("\n")
                        const actions = response.transaction.transaction.actions;
        })
})
                return res.send(time);
});
