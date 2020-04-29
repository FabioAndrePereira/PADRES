import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {baseURL} from '../../environments/environment';
import {catchError} from 'rxjs/operators';
import {Observable, throwError} from 'rxjs';

@Injectable()
export class PrincipleService {
    constructor(private http: HttpClient) { }
    
    getPrinciples(phID: number): Observable<any>{
        return this.http.get(baseURL + 'principles/' + phID).pipe(
            catchError(err =>  throwError(err))
        )
    }
    
    getRulesCountrySW(countryID: number): Observable<any>{
        return this.http.get(baseURL + 'rules/' + countryID).pipe(
            catchError(err =>  throwError(err))
        )
    }
    
    getSW(cID: number): Observable<any>{
        const endPoint = 'sw/' + cID;
        return this.http.get(baseURL + endPoint).pipe(
            catchError(err =>  throwError(err))
        )
    }
    
    getCountryBySW(swID: number): Observable<any>{
        return this.http.get(baseURL + 'country?sw=' + swID).pipe(
            catchError(err =>  throwError(err))
        )
    }
    
    // getPrinciplesHeader(): Observable<any>{
    //     return this.http.get(baseURL + 'principleH').pipe(
    //         catchError(err =>  throwError(err))
    //     )
    // }
    
    
    getCountry(): Observable<any>{
        return this.http.get(baseURL + 'country').pipe(
            catchError(err =>  throwError(err))
        )
    }
    
    postDataForm(data: any, swid: number, cID: number, opt): Observable<any>{
        const httpOptions2 = {
            headers: new HttpHeaders({ 'Content-Type': 'application/json' }),
            observe: 'response' as 'response'
        };
        data["doNMAP"] = opt.doNMAP;
		data["NMAPip"] = opt.NMAPip;
		data["ZAPurl"] = opt.ZAPurl;
		data["doZAP"] = opt.doZAP;
		const dataJSON = JSON.stringify(data);
        return  this.http.post(baseURL + 'postDataForm', dataJSON, httpOptions2).pipe(
            catchError(err =>  throwError(err))
        )
    }
    
}
