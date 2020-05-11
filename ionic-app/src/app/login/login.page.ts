import { catchError } from 'rxjs/operators';
import { Component, OnInit } from '@angular/core';
import {NgForm, FormGroup} from '@angular/forms';
import { User } from '../models/user';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';
import { LoadingController } from '@ionic/angular';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {
  data;
  form: FormGroup;
  constructor(
    public apiService: ApiService,
    public router: Router,
    public loadingController: LoadingController
  ) {
    // this.data = {
    //   email_address: '',
    //   pass_word: ''
    // };
    this.data = new User();
  }



  ngOnInit(){
  }

  
  onSubmit(myForm: NgForm) {
    console.log(myForm.value);
    this.showLoader();
    this.apiService.authLogin(myForm.value).subscribe((response) => {
      this.router.navigate(['tabs/tabs/tab1']);
      console.log(response); 
    });
  }

  async showLoader() {
    const loading = await this.loadingController.create({
      message: 'Signing in',
      duration: 5000,
      spinner: 'crescent'
    });
    await loading.present();
  }


  }


