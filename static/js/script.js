var predictBtn = document.getElementById("sub");
var out = document.getElementById("output");
var alt = document.getElementById("alert-placeholder");







async function Predict() {
    var res = {};
    var age = document.getElementById("age");
    var sex = document.getElementById("sex");
    var bmi = document.getElementById("bmi");
    var child = document.getElementById("children");
    var smoker = document.getElementById("smoker");
    var region = document.getElementById("region");


    console.log(age.value, bmi.value, sex.value, child.value, smoker.value, region.value);

    res['age'] = age.value
    res['sex'] = String(sex.value).toLowerCase();
    res['bmi'] = bmi.value;
    res['children'] = child.value;
    res['smoker'] = String(smoker.value).toLowerCase();
    res['region'] = String(region.value).toLowerCase();
    var url = 'https://testingapis12.herokuapp.com/predictmodel';

    alt.innerHTML = `
    <div class="alert alert-success alert-dismissible fade show" role="alert">
  <strong></strong>Submitted successfully!!
  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>
</div>
    `

    /*var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:5500/predictmodel', async = true);



    // In local files, status is 0 upon success in Mozilla Firefox
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            //document.getElementById("demo").innerHTML =
            console.log(this.response);

        };





    }

    xhr.setRequestHeader('Content-Type', 'application/json');
    console.log(res)
    xhr.send(JSON.stringify(res)); */

    const response = await fetch(url, {
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
        body: JSON.stringify(res) // body data type must match "Content-Type" header
    });

    // reset values
    age.value = "";
    sex.value = "";
    bmi.value = "";
    child.value = "";
    smoker.value = "";
    region.value = "";
    return response.json();




}




predictBtn.addEventListener("click", function (e) {
    e.preventDefault();

    Predict().then(res => {
        console.log(res)
        out.innerHTML = parseFloat(res['result']).toFixed(2) + ' INR'}
        )
})




