import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-tab2',
  templateUrl: './tab2.page.html',
  styleUrls: ['./tab2.page.scss'],
})
export class Tab2Page implements OnInit {
  mode;
  manual: boolean;
  hallLight;
  hallFan;
  kitchenLight;
  stove;
  coffee;
  pinmode;
  pin;


  constructor(private http: HttpClient) {
   }

  ngOnInit() {
  }

  updateMode(){
    if (this.manual === true){
      this.mode = 'manual';
    } else {
      this.mode = 'automatic';
    }
    // tslint:disable-next-line: deprecation
    this.http.get(`http://192.168.137.213:5000/controlmode/${this.mode}`).subscribe(response => {
      console.log(response);
    });
  }

  hl(){
    this.pin = 'HALL_LIGHT';
    if (this.hallLight === true){
      this.pinmode = 'True';
    } else {
      this.pinmode = 'False';
    }
    this.http.get(`http://192.168.137.213:5000/controls/${this.pin}/${this.pinmode}`).subscribe(response => {
      console.log(response);
  });
  }

  hf(){
    this.pin = 'HALL_FAN';
    if (this.hallFan === true){
      this.pinmode = 'True';
    } else {
      this.pinmode = 'False';
    }
    this.http.get(`http://192.168.137.213:5000/controls/${this.pin}/${this.pinmode}`).subscribe(response => {
      console.log(response);
  });
  }

  kl(){
    this.pin = 'KITCHEN_LIGHT';
    if (this.kitchenLight === true){
      this.pinmode = 'True';
    } else {
      this.pinmode = 'False';
    }
    this.http.get(`http://192.168.137.213:5000/controls/${this.pin}/${this.pinmode}`).subscribe(response => {
      console.log(response);
  });
  }

  stv(){
    this.pin = 'STOVE';
    if (this.stove === true){
      this.pinmode = 'True';
    } else {
      this.pinmode = 'False';
    }
    this.http.get(`http://192.168.137.140:5000/controls/${this.pin}/${this.pinmode}`).subscribe(response => {
      console.log(response);
  });
  }

  coffeemaker(){
    this.pin = 'coffee';
    if (this.coffee === true){
      this.pinmode = 'True';
    } else {
      this.pinmode = 'False';
    }
    this.http.get(`http://192.168.137.140:5000/controls/${this.pin}/${this.pinmode}`).subscribe(response => {
      console.log(response);
  });
  }

}
