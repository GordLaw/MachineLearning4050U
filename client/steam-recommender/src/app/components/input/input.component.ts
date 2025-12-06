import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { InputTextModule } from 'primeng/inputtext';
import { Button } from "primeng/button";
import { Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-input',
  imports: [FormsModule, InputTextModule, Button],
  templateUrl: './input.component.html',
  styleUrl: './input.component.css'
})
export class InputComponent {
  @Output() userInput = new EventEmitter<string>();
  value: string | undefined;

  onSubmit(form: any) {
    if (form.valid) {
      this.userInput.emit(this.value);
      form.resetForm()
    }
  }
}
