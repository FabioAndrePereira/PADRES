import {Component, OnDestroy, OnInit} from '@angular/core';
import { HistoryService} from './history.service';
import { ToastrService } from 'ngx-toastr';
import {interval, Observable, Subscription} from 'rxjs';

@Component({
	selector: 'app-history',
	templateUrl: './history.component.html',
	styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit, OnDestroy {
	constructor(
		private historyService: HistoryService,
		private toastr: ToastrService) { }

	displayedColumns: string[] = ['id', 'country', 'sw', 'name', 'timeStamp'];
	pdfsData: History[] = [];
	subSched: Subscription;
	ngOnInit() {
		let sub = this.historyService.getPdfs().subscribe(
			data => {
				this.pdfsData = data;
			},
			error => {
				console.log(error);
			},
			() => {}
		);
		//sub.unsubscribe();
		this.subSched = interval(60000).subscribe((val) => {
			this.historyService.getPdfs().subscribe(
				data => {
					this.pdfsData = data;
				},
				error => {
					console.log(error);
				},
				() => {}
			);
		});
	}
	displayPDF(row) {
		if (row.status == 0){
			this.toastr.info('PDF not available yet!');
		}
		else {
			this.historyService.getPDF(row.id).subscribe(
				data => {
					var blob = new Blob([data], {type: 'application/pdf'});
					var fileURL = URL.createObjectURL(blob);
					window.open(fileURL)
				},
				error => {
					console.log(error);
				},
				() => {}
			);
		}
	}

	ngOnDestroy(): void {
		this.subSched.unsubscribe();
	}

}

export interface History {
	id: number;
	country: string;
	sw: string;
	name: string;
	path: string;
	timeStamp: string;
}
