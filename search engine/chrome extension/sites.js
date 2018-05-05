
(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = 'jquery-1.9.0.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
/**
 * Stores the time that is spent on each site.
 *
 * The primary interface to this class is through setCurrentFocus.
 */
function Sites(config) {
  this._config = config;
  if (!localStorage.sites) {
    localStorage.sites = JSON.stringify({});
  }
  if(!localStorage.timeOfVisit) {
    localStorage.timeOfVisit = JSON.stringify({});
  }
  if(!localStorage.siteContent) {
    localStorage.siteContent = JSON.stringify({});
  }
  this._currentSite = null;
  this._siteRegexp = /^(\w+:\/\/[^\/]+).*$/;
  this._startTime = null;
}

/**
 * Returns a dictionary of site -> seconds.
 */
Object.defineProperty(Sites.prototype, "sites", {
  get: function() {
    var s = JSON.parse(localStorage.sites);
    var sites = {}
    for (var site in s) {
      if (s.hasOwnProperty(site) && !this._config.isIgnoredSite(site)) {
        sites[site] = s[site];
      }
    }
    return sites;
  }
});

/**
 * Returns a dictionary of site -> timeOfVisit.
 */
Object.defineProperty(Sites.prototype, "timeOfVisit", {
  get: function() {
    var s = JSON.parse(localStorage.timeOfVisit);
    var timeOfVisit = {}
    for (var site in s) {
      if (s.hasOwnProperty(site) && !this._config.isIgnoredSite(site)) {
        timeOfVisit[site] = s[site];
      }
    }
    return timeOfVisit;
  }
});

/**
 * Returns a dictionary of site -> siteContent.
 */
Object.defineProperty(Sites.prototype, "siteContent", {
  get: function() {
    var s = JSON.parse(localStorage.siteContent);
    var siteContent = {}
    for (var site in s) {
      if (s.hasOwnProperty(site) && !this._config.isIgnoredSite(site)) {
        siteContent[site] = s[site];
      }
    }
    return siteContent;
  }
});
/**
 * Returns just the site/domain from the url. Includes the protocol.
 * chrome://extensions/some/other?blah=ffdf -> chrome://extensions
 * @param {string} url The URL of the page, including the protocol.
 * @return {string} The site, including protocol, but not paths.
 */
Sites.prototype.getSiteFromUrl = function(url) {
  // var match = url.match(this._siteRegexp);
  // if (match) {
  //   return match[1];
  // }
  // return null;
  return url;
};

var postData = function(input, callback) {
  $.ajax({
      type: "GET",
      url: "http://127.0.0.1:5000/output",
      data: {data: input},
      // success: function(data) {
      //   console.log("inside the calldata");
      //   //alert(data);
      //   callback(data);
      // }
  });
} 
      
Sites.prototype._updateTime = function() {
  if (!this._currentSite || !this._startTime) {
    return;
  }
  var currentDate = new Date();
  var delta = currentDate - this._startTime;
  //console.log("Site: " + this._currentSite + " Delta = " + delta/1000);
  if (delta/1000/60 > 2 * this._config.updateTimePeriodMinutes) {
   // console.log("Delta of " + delta/1000 + " seconds too long; ignored.");
    return;
  }
  var sites = this.sites;
  var timeOfVisit = this.timeOfVisit;
  var siteContent = this.siteContent;
  //console.log(timeOfVisit)
  if (!sites[this._currentSite]) {
    sites[this._currentSite] = 0;
  }
  console.log('hello world');
  if(!timeOfVisit[this._currentSite]) {
    timeOfVisit[this._currentSite] = currentDate.toString();
    if (this._currentSite.indexOf("http://") == 0 ||
      this._currentSite.indexOf("https://") == 0) {
      postData(this._currentSite, function(data){
        // siteContent[this._currentSite] = data;
        // print(data);
        // console.log("hello,dl,h,les,;mlmmdsd,/hmh;kh ;,s /,hm;kword");
        // console.log(data);
      });
    }
    else {
      siteContent[this._currentSite] = "This is not a web page."
      // alert("This is not a web page.");
    }
  }
  sites[this._currentSite] += delta/1000;
  localStorage.sites = JSON.stringify(sites);
  localStorage.timeOfVisit = JSON.stringify(timeOfVisit);
  localStorage.siteContent = JSON.stringify(siteContent);
};

/**
 * This method should be called whenever there is a potential focus change.
 * Provide url=null if Chrome is out of focus.
 */
Sites.prototype.setCurrentFocus = function(url) {
  //alert("setCurrentFocus: " + JSON.stringify(this));
  this._updateTime();
  if (url == null) {
    this._currentSite = null;
    this._startTime = null;
    chrome.browserAction.setIcon(
        {path: {19: 'images/icon_paused19.png',
                38: 'images/icon_paused38.png'}});
  } else {
    this._currentSite = this.getSiteFromUrl(url);
    this._startTime = new Date();
    chrome.browserAction.setIcon(
        {path: {19: 'images/icon19.png',
                38: 'images/icon38.png'}});
  }
};

/**
 * Clear all statistics.
 */
Sites.prototype.clear = function() {
  localStorage.sites = JSON.stringify({});
  localStorage.timeOfVisit = JSON.stringify({});
  localStorage.siteContent = JSON.stringify({});
  this._config.lastClearTime = new Date().getTime();
};
