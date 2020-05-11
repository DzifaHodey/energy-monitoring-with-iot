import { Component, OnInit } from '@angular/core';
import {NgForm, FormGroup} from '@angular/forms';
import { MQTTService } from 'ionic-mqtt';

@Component({
  selector: 'app-tab3',
  templateUrl: './tab3.page.html',
  styleUrls: ['./tab3.page.scss'],
})
export class Tab3Page implements OnInit {
  ishidden;
  reportText;
  form: FormGroup;
  private _mqttClient: any;

  private MQTT_CONFIG: {
    host: string,
    port: number,
    clientId: string
    // path: string
  } = {
    host: '127.0.0.1',
    port: 9001,
    clientId: 'WebSocket'
    // path: '/mqtt'
  };

  private TOPIC: string[] = ['IssueReport'];

  constructor(private _mqttService: MQTTService)
 {
   this.ishidden = true;
   }

  ngOnInit() {
    this._mqttClient = this._mqttService.loadingMqtt(this._onConnectionLost, this._onMessageArrived, this.TOPIC, this.MQTT_CONFIG);
  }

  private _onConnectionLost(responseObject) {
    // connection listener
    // ...do actions when connection lost
    console.log('_onConnectionLost', responseObject);
  }

  private _onMessageArrived(message) {
    // message listener
    // ...do actions with arriving message
    console.log('message', message);
  }

  // public publishMessage() {
  //   console.log('publishMessage');

  //   this._mqttService.publishMessage(this.TOPIC[0], 'hello. COnnected');
  // }


  showhide() {
    if (this.ishidden === false) {
      this.ishidden = true;
    } else {
      this.ishidden = false;
    }
  }

  onReport(myReport: NgForm){
    const MESSAGE = this.reportText;
    this._mqttService.publishMessage(this.TOPIC[0], MESSAGE);
    this.ishidden = true;
    this.reportText = '';

  }


}



