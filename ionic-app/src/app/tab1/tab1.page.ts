import { Component, OnInit } from '@angular/core';
import { GoogleChartInterface } from 'ng2-google-charts';
import { User } from '../models/user';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-tab1',
  templateUrl: './tab1.page.html',
  styleUrls: ['./tab1.page.scss'],
})
export class Tab1Page implements OnInit {
  monthlyData;
  dailyData;
  devices;
  values;
  items;
  dataValues1;
  dailyTotal;
  public pieChart: GoogleChartInterface;
  public pieChart2: GoogleChartInterface;


  constructor(public apiService: ApiService, public router: Router) {
    this.monthlyData = [];
    this.dataValues1 = [];
    this.items = [];
    this.dailyData =[];
    this.devices = [];
    this.values = [];


  }

  ngOnInit() {
    this.getMonthlyCons();
    this.getDailyCons();
    this.loadSimplePieChart();
  }

  doRefresh(event) {
    console.log('Begin async operation');
    
    // event.target.complete();
    setTimeout(() => {
      this.monthlyData = [];
      this.dataValues1 = [];
      this.items = [];
      this.dailyData =[];
      this.devices = [];
      this.values = [];
      this.pieChart.dataTable = [];
      this.pieChart2.dataTable = [];
      this.getMonthlyCons();
      this.getDailyCons();
      this.loadSimplePieChart();
      console.log(this.pieChart.dataTable);
      console.log('Async operation has ended');
      event.target.complete();
    }, 3000);
  }

  getMonthlyCons() {
    // Get saved list of students
    this.apiService.getTotal().subscribe(response => {
      this.monthlyData = response;
      // console.log(this.monthlyData);
      // tslint:disable-next-line: forin
      for (const item in this.monthlyData) {
        const value = this.monthlyData[item];
        const key = item;
        this.items.push(key);
        this.dataValues1.push(value);
       }
      this.pieChart.dataTable.push([this.items[1], this.dataValues1[1]]);
      this.pieChart.dataTable.push([this.items[2], this.dataValues1[2]]);
      this.pieChart.dataTable.push([this.items[0], this.dataValues1[0]]);
      

      // console.log(this.pieChart.dataTable);
    });
  }


  getDailyCons() {
    // Get saved list of students
    this.apiService.getDaily().subscribe(response => {
      this.dailyData = response;
      // console.log(this.dailyData);

      // tslint:disable-next-line: forin
      for (const item1 in this.dailyData) {
        const value1 = this.dailyData[item1];
        const key1 = item1;
        this.devices.push(key1);
        this.values.push(value1);
       }
      this.pieChart2.dataTable.push([this.devices[1], this.values[1]]);
      this.pieChart2.dataTable.push([this.devices[0], this.values[0]]);
      this.pieChart2.dataTable.push([this.devices[2], this.values[2]]);
      this.pieChart2.dataTable.push([this.devices[3], this.values[3]]);
      this.pieChart2.dataTable.push([this.devices[4], this.values[4]]);
      this.pieChart2.dataTable.push([this.devices[5], this.values[5]]);
      this.pieChart2.dataTable.push([this.devices[6], this.values[6]]);

      this.dailyTotal = this.values[0] + this.values[2] + this.values[3] + this.values[4] + this.values[5] + this.values[6]
    });
  }



  loadSimplePieChart() {
    this.pieChart = {
      chartType: 'PieChart',
      dataTable: [],

      options: {
        // title: 'Consumption',
        height: 180,
        width: '100%',
        pieHole: 0.4,
        chartArea: {width: 260, height: 160},
        pieSliceText: 'value',
        pieSliceTextStyle: {fontSize: 12, suffix: 'W'},
        // suffix: 'W',
        legend: {textStyle: {fontSize: 11.5}}
        // tooltip: {trigger: 'focus', text: 'both'}
      },


    };

    this.pieChart2 = {
      chartType: 'PieChart',
      dataTable: [],

      options: {
        // title: 'Consumption',
        height: 180,
        width: '100%',
        pieHole: 0.4,
        chartArea: {width: 260, height: 160 } ,
        pieSliceTextStyle: {fontSize: 12},
        suffix: 'W',
        legend: {textStyle: {fontSize: 11.5}}
        // tooltip: {trigger: 'focus', text: 'both'}
        // pieSliceText: 'value'
      },

    };

    console.log('done');
  }


}

