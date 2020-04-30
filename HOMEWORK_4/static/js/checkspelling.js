 function spelling() {

    let text = document.getElementById("message");
    if (text == null) {
      console.log("NULL");
    } 
    else
    {
      execute(text);
    }

    function execute(text) {
      let https = require ('https');

      let host = 'api.cognitive.microsoft.com';
      let path = '/bing/v7.0/spellcheck';
      let key = 'e7894c840ce349edb4a8586b329d7244';

      let mkt = "en-US";
      let mode = "proof";
      let query_string = "?mkt=" + mkt + "&mode=" + mode;

      let request_params = {
          method : 'POST',
          hostname : host,
          path : path + query_string,
          headers : {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Content-Length' : text.length + 5,
            'Ocp-Apim-Subscription-Key': key,
          }
      };

      let response_handler = function (response) {
          let body_ = '';
          response.on ('data', function (d) {
              body_ += d;
          });
          response.on ('end', function () {
              let body = JSON.parse (body_);

              body["flaggedTokens"].forEach(function(element1) {
                  let word = "";
                  let max = 0;
                  element1["suggestions"].forEach(function(element2) {
                      if(element2["score"] > max) {
                          max = element2["score"];
                          word = element2["suggestion"];
                      }
                  })
                  text = text.replace(element1["token"], word);
              })
              document.getElementById("message").value = text;
          });
          response.on ('error', function (e) {
              console.log ('Error: ' + e.message);
          });
      };

      let req = https.request (request_params, response_handler);
      req.write ("text=" + text);
      req.end ();
    }
}

   function myFunction() {
    document.getElementById("message").value = "pii";
  }
