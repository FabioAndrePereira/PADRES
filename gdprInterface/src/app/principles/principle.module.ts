import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {TabViewModule} from 'primeng/tabview';
import {PrinciplesComponent} from './principles.component';
import {PrincipleService} from './principle.service';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatListModule} from '@angular/material/list';
import {ToggleButtonModule} from 'primeng/togglebutton';
import {MatCheckboxModule, MatDialogModule, MatInputModule, MatSelectModule} from '@angular/material';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {ModalconfimComponent} from './modalconfim/modalconfim.component';


@NgModule({
    declarations: [
        PrinciplesComponent,
		ModalconfimComponent
    ],
	imports: [
		CommonModule,
		TabViewModule,
		ReactiveFormsModule,
		MatListModule,
		ToggleButtonModule,
		MatSelectModule,
		FormsModule,
		BrowserAnimationsModule,
		MatDialogModule,
		MatCheckboxModule,
		MatInputModule
	],
    providers: [
        PrincipleService
    ],
    entryComponents: [
    	ModalconfimComponent
    ]
})
export class PrincipleModule { }
