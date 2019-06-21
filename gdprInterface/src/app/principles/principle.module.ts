import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {TabViewModule} from 'primeng/tabview';
import {PrinciplesComponent} from './principles.component';
import {PrincipleService} from './principle.service';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatListModule} from '@angular/material/list';
import {ToggleButtonModule} from 'primeng/togglebutton';
import {MatSelectModule} from '@angular/material';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

@NgModule({
    declarations: [
        PrinciplesComponent
    ],
    imports: [
        CommonModule,
        TabViewModule,
        ReactiveFormsModule,
        MatListModule,
        ToggleButtonModule,
        MatSelectModule,
        FormsModule,
        BrowserAnimationsModule
    ],
    providers: [
        PrincipleService
    ],
    entryComponents: [
    ]
    
})
export class PrincipleModule { }
