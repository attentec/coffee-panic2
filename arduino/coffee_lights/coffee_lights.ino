#include <FastLED.h>
#define NUM_LEDS 59
#define LED_PIN 4

#define MAX_HUE 64 // 64 = green, 0 = red

#define MAX_BRIGHTNESS 127
#define MIN_BRIGHTNESS 0

#define FULL_CUTOFF 1.0
#define EMPTY_CUTOFF 0.1
#define PARTY_CUTOFF 0.95

#define ANIM_STEP 0.002

struct CRGB leds[NUM_LEDS];
struct CHSV hsvLeds[NUM_LEDS];

float targetPercent = 0.0f;
float currentPercent = 0.0;

float hue_interpolation_constant = 1 / (FULL_CUTOFF - EMPTY_CUTOFF);

float percentage = 0;

void setup() {
    FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
    FastLED.clear();
    FastLED.show();
    // FastLED.setBrightness(16);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        targetPercent = Serial.parseFloat();
    }

    if (targetPercent < currentPercent) {
        currentPercent -= ANIM_STEP;
        if (targetPercent > currentPercent) {
            currentPercent = targetPercent;
        }
    } else if (targetPercent > currentPercent) {
        currentPercent += ANIM_STEP;
        if (targetPercent < currentPercent) {
            currentPercent = targetPercent;
        }
    }

    if (currentPercent > PARTY_CUTOFF) {
        CHSV hsv;
        hsv.hue = beat8(25, 255);
        hsv.sat = 255;
        hsv.val = MAX_BRIGHTNESS;
        for( int i = 0; i < NUM_LEDS; ++i) {
            hsvLeds[i] = hsv;
            hsv.hue += 2;
        }
        hsv2rgb_raw(hsvLeds, leds, NUM_LEDS);
        FastLED.show();
    } else if (currentPercent <= 0.05) {
        setLedColors(0, NUM_LEDS, CHSV(0, 255, 4));
    } else {
        calculateAndSetColors();
    }
}

void calculateAndSetColors() {
    float led_brightness = currentPercent * NUM_LEDS;
    uint8_t fully_on_leds = floor(led_brightness);
    float last_led_percentage = led_brightness - fully_on_leds;

    uint8_t current_hue = interpolate_hue(currentPercent);

    // The LED bar is mounted upside down, so the array is populated from the back
    for (int i=0; i<NUM_LEDS; i++) {
        if (i < fully_on_leds) {
            hsvLeds[NUM_LEDS-i-1] = CHSV(current_hue, 255, MAX_BRIGHTNESS);
        } else if (i == fully_on_leds) {
            // TODO: Set min brightness
            hsvLeds[NUM_LEDS-i-1] = CHSV(current_hue, 255, max(MIN_BRIGHTNESS, last_led_percentage * MAX_BRIGHTNESS));
        } else {
            hsvLeds[NUM_LEDS-i-1] = CHSV(current_hue, 255, MIN_BRIGHTNESS);
        }
    }
    hsv2rgb_raw(hsvLeds, leds, NUM_LEDS);
    FastLED.show();
}

void setLedColors(int start, int end, CHSV color) {
    for (int i=start; i<end; i++) {
        hsvLeds[i] = color;
    }
    hsv2rgb_raw(hsvLeds, leds, NUM_LEDS);
    FastLED.show();
}

uint8_t interpolate_hue(float percent) {
    // Clamp percentage to EMPTY_CUTOFF <= percent <= FULL_CUTOFF and shift it to 0
    float converted_percent = min(max(percent, EMPTY_CUTOFF), FULL_CUTOFF) - EMPTY_CUTOFF;

    // Multiply the converted percentage with the interpolation constant
    return hue_interpolation_constant * converted_percent * MAX_HUE;
}
