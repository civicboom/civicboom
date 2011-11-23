if(!('boom' in window))
  boom = {};

if(!('boom_development' in window) || !('console' in window) || !console.log)
  console = {
    log: function () {}
  }

boom.init_foot = [];
