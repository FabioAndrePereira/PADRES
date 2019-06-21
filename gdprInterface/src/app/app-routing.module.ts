import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {PrinciplesComponent} from './principles/principles.component';
import {HomeComponent} from './home/home.component';

const routes: Routes = [
  { path: 'gdpr/new', component: PrinciplesComponent },
  { path: 'home', component: HomeComponent  },
  { path: '', redirectTo: 'home', pathMatch: 'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
