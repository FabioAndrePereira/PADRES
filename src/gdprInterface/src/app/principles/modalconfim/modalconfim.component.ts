import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material';
import {FormControl, Validators} from '@angular/forms';

@Component({
	selector: 'app-modalconfim',
	templateUrl: './modalconfim.component.html',
	styleUrls: ['./modalconfim.component.css']
})
export class ModalconfimComponent implements OnInit {
	dozap: FormControl;
	constructor(
		public dialogRef: MatDialogRef<ModalconfimComponent>,
		@Inject(MAT_DIALOG_DATA) public data: any,
	) {
		this.dozap = new FormControl('');
	}

	changeForm(){
		if(this.dozap) {
			const validators = [Validators.required, Validators.pattern("https?:\\/\\/.*\\/$") ];
			this.dozap.setValidators(validators);
		}
		else{
			this.dozap.clearValidators();
			this.dozap.setValue('')
		}
	}



	ngOnInit() {
	}


	onNoClick(): void {
		this.dialogRef.close(0);
	}


}
