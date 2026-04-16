// Surge/QX compatible PingMe script
// Generated from upstream PingMe.js via scripts/build_pingme_surge.py

const isSurge = typeof $persistentStore !== 'undefined';
const isQX = typeof $prefs !== 'undefined';

const store = {
  read(key) {
    if (isSurge) return $persistentStore.read(key);
    if (isQX) return $prefs.valueForKey(key);
    return null;
  },
  write(val, key) {
    if (isSurge) return $persistentStore.write(val, key);
    if (isQX) return $prefs.setValueForKey(val, key);
    return false;
  }
};

function notify(title, subtitle, body) {
  if (typeof $notification !== 'undefined') return $notification.post(title, subtitle, body);
  if (typeof $notify !== 'undefined') return $notify(title, subtitle, body);
}

function done(value) {
  if (typeof $done !== 'undefined') $done(value);
}

function stableStringify(obj) {
  if (obj === null || typeof obj !== 'object') return JSON.stringify(obj);
  if (Array.isArray(obj)) return '[' + obj.map(stableStringify).join(',') + ']';
  return '{' + Object.keys(obj).sort().map(k => JSON.stringify(k) + ':' + stableStringify(obj[k])).join(',') + '}';
}

function requestGet(options) {
  return new Promise((resolve, reject) => {
    if (typeof $task !== 'undefined') {
      $task.fetch({ method: 'GET', ...options }).then(resolve).catch(reject);
      return;
    }
    if (typeof $httpClient !== 'undefined') {
      $httpClient.get(options, (error, response, data) => {
        if (error) return reject({ error: String(error) });
        resolve({
          statusCode: response && (response.status || response.statusCode),
          headers: response ? response.headers : {},
          body: data
        });
      });
      return;
    }
    reject({ error: 'No HTTP client available' });
  });
}

