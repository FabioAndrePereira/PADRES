import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {PrinciplesComponent} from './principles/principles.component';
import {HomeComponent} from './home/home.component';
import {HistoryComponent} from './history/history.component';

const routes: Routes = [
  { path: 'gdpr/new', component: PrinciplesComponent },
  { path: 'gdpr/history', component: HistoryComponent},
  { path: 'home', component: HomeComponent  },
  { path: '', redirectTo: 'gdpr/history', pathMatch: 'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
