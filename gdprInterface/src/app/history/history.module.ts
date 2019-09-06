import {NgModule} from '@angular/core';
import {HistoryComponent} from './history.component';
import {MatTableModule} from '@angular/material/table';
import {HistoryService} from './history.service';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

@NgModule({
	declarations: [
		HistoryComponent
	],
	imports: [
		BrowserAnimationsModule,
		MatTableModule
	],
	providers: [
		HistoryService
	],
	entryComponents: [
	]
})

export  class HistoryModule { }
