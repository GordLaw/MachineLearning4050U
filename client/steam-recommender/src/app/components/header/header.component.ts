import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { MenubarModule } from 'primeng/menubar';
import { MenuItem } from 'primeng/api';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-header',
  imports: [MenubarModule, ButtonModule],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css',
})
export class HeaderComponent implements OnInit {
    @Output() newItemEvent = new EventEmitter<string>();
    items: MenuItem[] | undefined;

    ngOnInit() {
        this.items = [
            {
                label: 'Home',
                command: () => { this.newItemEvent.emit("container"); }
            },
            {
                label: 'Featured',
                command: () => { this.newItemEvent.emit('featuredContainer'); }
            },
            {
                label: 'About',
                command: () => { this.newItemEvent.emit('aboutContainer'); }
            }
        ];
    }
}
