import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';

@Component({
	selector: 'app-modalconfim',
	templateUrl: './modalconfim.component.html',
	styleUrls: ['./modalconfim.component.css']
})
export class ModalconfimComponent implements OnInit {

	constructor(
		public dialogRef: MatDialogRef<ModalconfimComponent>,
		@Inject(MAT_DIALOG_DATA) public data: any) { }



	ngOnInit() {
	}

	onNoClick(): void {
		this.dialogRef.close();
	}


}
