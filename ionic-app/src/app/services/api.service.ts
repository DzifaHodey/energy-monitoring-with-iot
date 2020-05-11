import { TotalCon } from './../models/total-con';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { User } from '../models/user';
import { Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';
import { Daily } from '../models/daily';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  base_path = 'http://127.0.0.1:5000';
  // base_path = 'http://192.168.137.213:5000';
  constructor(private http: HttpClient) { }

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  // // Handle API errors
  handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
      return throwError('Something bad happened; please try again later.');
    } else if (error.status != 200) {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      console.error(
            `Backend error ${error.status}` +
            `body was: ${error.error}`);
      return throwError('Something bad happened; please try again later.');
          }
    if (error.status == 200) {
        return '200';
      }
    }
    // return an observable with a user-facing error message



    authLogin(item): Observable<any> {
      return this.http
        .post<User>(this.base_path + '/login', JSON.stringify(item), this.httpOptions)
        .pipe(
          retry(2),
          catchError(this.handleError)
        )
    }

    getTotal(): Observable<any> {
      return this.http
        .get<TotalCon>(this.base_path + '/consumption/total/2020-04/50')
        .pipe(
          retry(2),
          catchError(this.handleError)
        )
    }

    getDaily(): Observable<any> {
      return this.http
        .get<Daily>(this.base_path + '/consumption/daily/2020-04-26')
        .pipe(
          retry(2),
          catchError(this.handleError)
        )
    }

    // controlMode(): Observable<any> {
    //   return this.http
    //     .get<Daily>(this.base_path + '/control/')
    //     .pipe(
    //       retry(2),
    //       catchError(this.handleError)
    //     )
    // }

  }
