import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';
import { IonicModule } from '@ionic/angular';

import { TabsPageRoutingModule } from './tabs-routing.module';

import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: 'tabs',
    component: TabsPage,
    children: [
        // { path: 'tab1', loadChildren: '../tab1/tab1.module#Tab1PageModule'},
        { path: 'tab1', loadChildren: () => import('../tab1/tab1.module').then( m => m.Tab1PageModule)},
        { path: 'tab2', loadChildren: () => import('../tab2/tab2.module').then( m => m.Tab2PageModule)},
        { path: 'tab3', loadChildren: () => import('../tab3/tab3.module').then( m => m.Tab3PageModule)},
    ]
  },
  {
    path: '',
    redirectTo: '/tabs/tabs/tab1',
    // pathMatch:'full'
  }
];


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes),
    TabsPageRoutingModule
  ],
  declarations: [TabsPage]
})
export class TabsPageModule {}
