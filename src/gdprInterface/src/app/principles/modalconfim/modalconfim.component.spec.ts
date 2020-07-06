import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModalconfimComponent } from './modalconfim.component';

describe('ModalconfimComponent', () => {
  let component: ModalconfimComponent;
  let fixture: ComponentFixture<ModalconfimComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModalconfimComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModalconfimComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
