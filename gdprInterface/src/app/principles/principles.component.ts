import {Component, OnInit} from '@angular/core';
import {MenuItem} from 'primeng/api';
import {PrincipleService} from './principle.service';
import {Principle} from './principle';
import {FormArray, FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import {ModalconfimComponent} from './modalconfim/modalconfim.component';
import {MatDialog} from '@angular/material';
import {Dialog} from 'primeng/dialog';


export interface DialogData {
	doNMAP: boolean;
	NMAPaddress: string;
	ZAPURL: string;
}

@Component({
    selector: 'app-rules',
    templateUrl: './principles.component.html',
    styleUrls: ['./principles.component.css']
})
export class PrinciplesComponent implements OnInit {
    principles: MenuItem[] = [
        {label: 'Lawfulness, fairness and transparency', id: '1'},
        {label: 'Purpose limitation', id: '2'},
        {label: 'Data minimisation', id: '3'},
        {label: 'Accuracy', id: '4'},
        {label: 'Storage limitation', id: '5'},
        {label: 'Integrity and confidentiality ', id: '6'},
        {label: 'Accountability', id: '7'},
        {label: 'Rules Specific for the selected country', id: '8'},

    ];
    principlesR: Principle[] = [];
    sw: iSW[] = [];
    country: iCountry[] = [];

    formP: FormGroup;
    formPrincipleArray: FormArray;
    formRuleArray: FormArray;

    selectedCountry: number;
    selectedSW: number;

    constructor(
    	private principleService: PrincipleService,
		private fb: FormBuilder,
		private router: Router,
		private toastr: ToastrService,
		private modalDialog: MatDialog
	) {
        this.createForm();
    }

    ngOnInit() {
        this.getCountry();
        this.getSW(0);
        this.getPrinciples();
    }

    getCountry() {
        this.principleService.getCountry().subscribe(
            data => {
                data.forEach( country  => {
                    const obj = {id: country.cID, name: country.cName, abvr: country.cAcronym};
                    this.country.push(obj);
                });
            }
        );
    }
    getSW(cID: number) {
        this.principleService.getSW(cID).subscribe(
            data => {
                data.forEach( d => {
                    const obj: iSW = {id: d.id, desc: d.description};
                    this.sw.push(obj);
                    });
            }
        );
    }

    getPrin8() {
        const controlArrayM = this.formP.get('principle') as FormArray;
        this.principleService.getRulesCountrySW(this.selectedCountry).subscribe(
            data => {
                data.forEach((d: any, index1) => {
                    const obs = new Principle(d.rID, d.rDefinition);
                    obs.principleHeaderID = 8;
                    this.principlesR.push(obs);
                    this.addRule(7);
                    const controlArray = controlArrayM.controls[7].get('rules') as FormArray;
                    controlArray.controls[index1].get('ruleID').setValue(obs.id);
                    controlArray.controls[index1].get('ruleDef').setValue(obs.definition);
                    controlArray.controls[index1].get('ruleCheck').setValue(false);
                });
            }
        );
    }

    getPrinciples() {
        this.principles.forEach((principle, index) => {
            this.addPrinciple();
            const controlArrayM = this.formP.get('principle') as FormArray;
            controlArrayM.controls[index].get('pID').setValue(principle.id);
            if (principle.id != '8') { // 8th principle is a diff table
                this.principleService.getPrinciples(parseInt(principle.id)).subscribe(
                    (data: Principle[]) => {
                        data.forEach((d: any, index1) => {
                            const obs = new Principle(d.pID, d.pDefinition);
                            obs.principleHeaderID = parseInt(principle.id);
                            this.principlesR.push(obs);
                            this.addRule(index);
                            const controlArray = controlArrayM.controls[index].get('rules') as FormArray;
                            controlArray.controls[index1].get('ruleID').setValue(obs.id);
                            controlArray.controls[index1].get('ruleDef').setValue(obs.definition);
                            controlArray.controls[index1].get('ruleCheck').setValue(false);
                        });
                    },
                    error1 => {
                        console.log(error1);
                    }
                );
            }

        });
    }

    createForm() {
        this.formP = this.fb.group({
            country: [Validators.required],
            sw: [Validators.required],
            principle: this.fb.array([])
        });
    }

    createPrinciple() {
        return this.fb.group({
            pID: ['', Validators.required],
            rules: this.fb.array([])
        });
    }

    addPrinciple() {
        this.formPrincipleArray = this.formP.get('principle') as FormArray;
        this.formPrincipleArray.push(this.createPrinciple());
    }

    createRule() {
        return this.fb.group({
            ruleID: ['', Validators.required],
            ruleDef: ['', Validators.required],
            ruleCheck: [false, Validators.required]
        });
    }

    addRule(i: number) {
        this.formRuleArray = (this.formP.get('principle') as FormArray).at(i).get('rules') as FormArray;
        this.formRuleArray.push(this.createRule());
    }

    submitData() {
        const formD = this.formP.value;
        let doNMAP = false;
        let doZAP = false;
        let NMAPip = '';
        let ZAPurl = '';
		const dialogRef = this.modalDialog.open(ModalconfimComponent, {
			width: '350px',
			data: { doNMAP: doNMAP, NMAPip: NMAPip, ZAPurl: ZAPurl, doZAP: doZAP}
		});
		dialogRef.afterClosed().subscribe(result => {
			if ( result == 0 )
				console.log("result");
			else {
				//console.log(result);
				this.principleService.postDataForm(formD, this.selectedSW, this.selectedCountry, result).subscribe(
					data => {
						this.toastr.success('Data sent successfully');
					},
					error1 => {
						console.log(error1);
						this.toastr.error('Error sending data' + error1.message);
					},
					() => {
						this.formP.reset();
						this.router.navigate(['gdpr/history']);
					}
				);
			}
		});
    }

    managePrin() {
        // remove rules where princ 8
        this.principlesR = this.principlesR.filter( prin => prin.principleHeaderID != 8);
        const l = this.getRulesArrayF().length;
        for (let i = 0; i < l ; i++) {
            this.getRulesArrayF().removeAt(0);
        }

    }

    getRulesArrayF() {
        return (this.formP.get('principle') as FormGroup).controls[7].get('rules') as FormArray;
    }

    updateCountryList() {
        // this.country = [];
    }

    updateSWlist() { // update sw list and also get rules for this country
        this.sw = [];
        this.getSW(this.selectedCountry);
        this.managePrin();
        this.getPrin8();
    }

    submitCheck() {
        return this.selectedCountry > 0 && this.selectedSW > 0;
    }

}

export interface iSW {
    id: number;
    desc: string;

}
export interface iCountry {
    id: number;
    name: string;
    abvr: string;
}

export interface modalConfirmData {
	ipAdress: string;
	webAppURL: string;
	doNmap: boolean;
}
