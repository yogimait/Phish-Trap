// var results = {};
// var legitimatePercents = {};
// var isPhish = {};


// function fetchLive(callback) {
//   fetch(chrome.runtime.getURL('static/classifier.json'))
//     .then(function(response) { 
//       if (!response.ok) { throw response }
//       return response.json(); 
//     })
//     .then(function(data) {
//       chrome.storage.local.set({cache: data, cacheTime: Date.now()}, function() {
//         callback(data);
//       });
//     });
// }


// function fetchCLF(callback) {
//   chrome.storage.local.get(['cache', 'cacheTime'], function(items) {
//       if (items.cache && items.cacheTime) {
//           return callback(items.cache);
//       }
//       fetchLive(callback);
//   });
// }

// function openInDocker(url, tabId) {
//   // Configuration for your existing Docker container
//   const containerId = '8dde013a24ad64f385d812132ead484420011704f9091f80ef6e73c9bc9f8d5d'; // Replace with your container name
//   const containerPort = '5901'; // Replace with your container's exposed port

//   // Format the URL for Docker container
//   const dockerUrl = `http://localhost:${containerPort}?url=${encodeURIComponent(url)}`;
  
//   // Open the URL in a new tab
//   chrome.tabs.create({ url: dockerUrl }, function(tab) {
//     console.log('Opened in Docker container:', dockerUrl);
//   });
// };

// function classify(tabId, result) {
//   var legitimateCount = 0;
//   var suspiciousCount = 0;
//   var phishingCount = 0;

//   for(var key in result) {
//     if(result[key] == "1") phishingCount++;
//     else if(result[key] == "0") suspiciousCount++;
//     else legitimateCount++;
//   }
//   legitimatePercents[tabId] = legitimateCount / (phishingCount+suspiciousCount+legitimateCount) * 100;

//   if(result.length != 0) {
//     var X = [];
//     X[0] = [];
//     for(var key in result) {
//         X[0].push(parseInt(result[key]));
//     }
//     console.log(result);
//     console.log(X);
//     fetchCLF(function(clf) {
//       var rf = random_forest(clf);
//       y = rf.predict(X);
//       console.log(y[0]);
//       if(y[0][0]) {
//         isPhish[tabId] = true;
//       } else {
//         isPhish[tabId] = false;
//       }
//       chrome.storage.local.set({'results': results, 'legitimatePercents': legitimatePercents, 'isPhish': isPhish});

//       if (isPhish[tabId]) {
//         chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
//           chrome.tabs.sendMessage(tabs[0].id, {action: "alert_user"}, function(response) {
//             if (confirm('Do you want to open this site in a secure Docker container?')) {
//               // Get current URL and open in Docker
//               openInDocker(tabs[0].url, tabs[0].id);
//             } else {
//               // Go back to previous page if user declines
//               chrome.tabs.goBack(tabs[0].id);
//             }
//           });
//         });
//       }
//     });
//   }

// }

// chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
//   results[sender.tab.id]=request;
//   classify(sender.tab.id, request);
//   sendResponse({received: "result"});
// });




var results = {};
var legitimatePercents = {};
var isPhish = {};

function fetchLive(callback) {
  fetch(chrome.runtime.getURL('static/classifier.json'))
    .then(function(response) { 
      if (!response.ok) { throw response }
      return response.json(); 
    })
    .then(function(data) {
      chrome.storage.local.set({cache: data, cacheTime: Date.now()}, function() {
        callback(data);
      });
    });
}

function fetchCLF(callback) {
  chrome.storage.local.get(['cache', 'cacheTime'], function(items) {
      if (items.cache && items.cacheTime) {
          return callback(items.cache);
      }
      fetchLive(callback);
  });
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.skip) {
    console.log("Skipped phishing check for localhost:6080");
    sendResponse({ received: "skipped" });
    return;
  }
  
  results[sender.tab.id] = request;
  classify(sender.tab.id, request);
  sendResponse({ received: "result" });
});


function openInDocker(url, tabId) {
  const containerPort = '6080';
  const dockerUrl = `http://localhost:${containerPort}/?url=${encodeURIComponent(url)}`;
  
  chrome.tabs.create({ url: dockerUrl }, function(tab) {
    console.log('Opened in Docker container:', dockerUrl);
  });

}

function classify(tabId, result) {
  var legitimateCount = 0;
  var suspiciousCount = 0;
  var phishingCount = 0;

  for(var key in result) {
    if(result[key] == "1") phishingCount++;
    else if(result[key] == "0") suspiciousCount++;
    else legitimateCount++;
  }
  legitimatePercents[tabId] = legitimateCount / (phishingCount+suspiciousCount+legitimateCount) * 100;

  if(result.length != 0) {
    var X = [];
    X[0] = [];
    for(var key in result) {
        X[0].push(parseInt(result[key]));
    }
    
    fetchCLF(function(clf) {
      var rf = random_forest(clf);
      y = rf.predict(X);
      if(y[0][0]) {
        isPhish[tabId] = true;
      } else {
        isPhish[tabId] = false;
      }
      chrome.storage.local.set({'results': results, 'legitimatePercents': legitimatePercents, 'isPhish': isPhish});

      if (isPhish[tabId]) {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          // First show warning alert
          chrome.tabs.sendMessage(tabs[0].id, {action: "alert_user"}, function(response) {
            // After first alert, show Docker prompt
            chrome.tabs.sendMessage(tabs[0].id, {action: "show_docker_confirm"}, function(response) {
              if (response && response.confirm) {
                openInDocker(tabs[0].url, tabs[0].id);
              } else {
                chrome.tabs.goBack(tabs[0].id);
              }
            });
          });
        });
      }
    });
  }
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  results[sender.tab.id]=request;
  classify(sender.tab.id, request);
  sendResponse({received: "result"});
});