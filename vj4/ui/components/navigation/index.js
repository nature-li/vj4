import _ from 'lodash';
import responsiveCutoff from 'vj/breakpoints.json';
import { isBelow } from 'vj/utils/mediaQuery';

class MultipleStateContainer {
  constructor(onStateChange, initialState = false) {
    this.onStateChange = onStateChange;
    this.states = {};
    this.currentState = initialState;
  }

  set(name, value, update = true) {
    this.states[name] = value;
    if (update) {
      this.update();
    }
  }

  get(name) {
    return this.states[name];
  }

  update() {
    const newState = this.getState();
    if (newState !== this.currentState) {
      this.onStateChange(newState);
      this.currentState = newState;
    }
  }

  getState() {
    return _.values(this.states).indexOf(true) > -1;
  }
}

class Navigation {
  constructor($nav, $navShadow) {
    this.updateExpandWidth = _.throttle(this.updateExpandWidthImmediate.bind(this), 200);
    this.$nav = $nav;
    this.$navRow = $nav.children('.row');
    this.$navShadow = $navShadow;
    this.floating = new MultipleStateContainer(this.updateFloating.bind(this), true);
    this.logoVisible = new MultipleStateContainer(this.updateLogoVisibility.bind(this), true);
    this.expanded = new MultipleStateContainer(this.updateExpandState.bind(this));
    // this.setFloating();
    // this.setLogoVisibility();
  }

  setFloating() {
    if (!this.$nav.hasClass('floating')) {
      this.$nav.addClass('floating');
    }

    if (!this.$navShadow.hasClass('floating')) {
      this.$navShadow.addClass('floating');
    }

    if (!$('body').hasClass('nav--floating')) {
      $('body').addClass('nav--floating');
    }
  }

  updateFloating(state) {
    this.setFloating();
    // if (state) {
    //   this.$nav.addClass('floating');
    //   this.$navShadow.addClass('floating');
    //   $('body').addClass('nav--floating');
    // } else {
    //   this.$nav.removeClass('floating');
    //   this.$navShadow.removeClass('floating');
    //   $('body').removeClass('nav--floating');
    // }
  }

  setLogoVisibility() {
    if (!this.$nav.hasClass('showlogo')) {
      this.$nav.addClass('showlogo');
    }
  }

  updateLogoVisibility(state) {
    this.setLogoVisibility();
    // if (state) {
    //   this.$nav.addClass('showlogo');
    // } else {
    //   this.$nav.removeClass('showlogo');
    // }
  }

  updateExpandWidthImmediate() {
    this.$navRow.css('max-width', `${window.innerWidth}px`);
  }

  updateExpandState(state) {
    if (state) {
      $(window).on('resize', this.updateExpandWidth);
      this.updateExpandWidthImmediate();
    } else {
      $(window).off('resize', this.updateExpandWidth);
      this.$navRow.css('max-width', '');
    }
  }

  getHeight() {
    if (isBelow(responsiveCutoff.mobile)) {
      return 0;
    }
    if (this.$nav.length === 0) {
      return 0;
    }
    if (!this._navHeight) {
      this._navHeight = this.$nav.height();
    }
    return this._navHeight;
  }
}

Navigation.instance = new Navigation($('.nav'), $('.nav--shadow'));

export default Navigation;
