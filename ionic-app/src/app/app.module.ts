import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';

import { IonicModule, IonicRouteStrategy } from '@ionic/angular';
import { SplashScreen } from '@ionic-native/splash-screen/ngx';
import { StatusBar } from '@ionic-native/status-bar/ngx';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { IonicStorageModule } from '@ionic/storage';
import {HttpClientModule} from '@angular/common/http';
import { IonicMqttModule, MQTTService } from 'ionic-mqtt';

// import { MqttModule, IMqttServiceOptions, MqttService } from 'ngx-mqtt';
// export const MQTT_SERVICE_OPTIONS: IMqttServiceOptions = {
//   hostname: 'localhost',
//   port: 1883,
//   path: '/mqtt'
// };

@NgModule({
  declarations: [AppComponent],
  entryComponents: [],
  imports: [BrowserModule,
    IonicModule.forRoot(),
    AppRoutingModule,
    IonicStorageModule.forRoot(),
    HttpClientModule,
    IonicMqttModule,
    // MqttModule.forRoot(MQTT_SERVICE_OPTIONS)
  ],
  providers: [
    StatusBar,
    SplashScreen,
    MQTTService,
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
