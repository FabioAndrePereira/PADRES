import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable, throwError} from 'rxjs';
import {baseURL} from '../../environments/environment';
import {catchError} from 'rxjs/operators';
import {History} from './history.component';


@Injectable()
export class HistoryService {
	constructor(private http: HttpClient) { }
	
	getPdfs(): Observable<History[]> {
		return this.http.get<History[]>(baseURL + 'getPDFs').pipe(
			catchError(err => throwError(err))
		);
	}
}
