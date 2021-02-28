var train_admin = document.getElementById('train_admin');
var pred_admin = document.getElementById('pred_admin');
console.log(pred_admin)



const selectedFile = document.getElementById('input_train')
const selectedFile1 = document.getElementById('input_pred')



train_admin.addEventListener("click",function(e){
   
    

    console.log(selectedFile.value);
    var url = 'http://127.0.0.1:5500/train';


    var payload = {};
    payload["folderPath"] = String(selectedFile.value);
    console.log(payload)

    var r = fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        // *default, no-cache, reload, force-cache, only-if-cached
        // include, *same-origin, omit
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer',
        // manual, *follow, error
        // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(payload) // body data type must match "Content-Type" header
    });

    r.then(res => res.json()).then(res => console.log(res));



});



// Predictions
pred_admin.addEventListener("click",function(e){
   
    
    console.log("Heel");
    console.log(selectedFile1.value);
    var url = 'http://127.0.0.1:5500/predict';


    var payload = {};
    payload["folderPath"] = String(selectedFile1.value);
    console.log(payload)

    var r = fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        // *default, no-cache, reload, force-cache, only-if-cached
        // include, *same-origin, omit
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer',
        // manual, *follow, error
        // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(payload) // body data type must match "Content-Type" header
    });

    r.then(res => {
        console.log(res);
    })
})



