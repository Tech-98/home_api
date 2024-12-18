const ewelink = require('ewelink-api');
const express = require('express');


(async () => {

  const connection = new ewelink({
    email: 'saif.ally1998@gmail.com',
    password: 'Agent@98',
    region: 'eu',
    APP_ID: 'Uw83EKZFxdif7XFXEsrpduz5YyjP7nTl',
    APP_SECRET: 'mXLOjea0woSMvK9gw7Fjsy7YlFO4iSu6'
  });
  const app = express ();
  app.use(express.json());
  app.get("/status", (request, response) => {
      const status = {
         "Status": "Running2"
      };
      
      response.send(status);
   });
   app.get("/switch", async (request, response) => {
    const status = {
       "Status": "Running2"
    };

    const device = await connection.getDevice('100145d4cc');
    console.log(device);

    /* toggle device */
    await connection.toggleDevice('100145d4cc');
    
    response.send(status);
 });

//  app.listen(3430, '127.0.0.1');
  app.listen(3430, '127.0.0.1');
})();



      /* get all devices */
//   const devices = await connection.getDevices();
//   console.log(devices);

    /* get specific devide info */