import { Component, OnInit } from '@angular/core';
import {HistoryService} from './history.service';


@Component({
	selector: 'app-history',
	templateUrl: './history.component.html',
	styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {
	constructor(private historyService: HistoryService) { }
	displayedColumns: string[] = ['id', 'country', 'sw', 'name', 'timeStamp'];
	pdfsData: History[] = [];
	hover = false;
	pdfBLOBurl;
	ngOnInit() {
		this.historyService.getPdfs().subscribe(
			data => {
				this.pdfsData = data;
			},
			error => {
				console.log(error);
			},
			() => {}
		);
	}
	displayPDF(row) {
		this.historyService.getPDF().subscribe(
			data => {
				console.log(data)
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
	// changeBG() {
	// 	this.over ? this.over = false : this.over = true;
	// }
}

export interface History {
	id: number;
	country: string;
	sw: string;
	name: string;
	path: string;
	timeStamp: string;
}
